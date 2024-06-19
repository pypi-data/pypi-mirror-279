import math
import warnings
from abc import ABC, abstractmethod
from copy import deepcopy
from distutils.version import LooseVersion

import CaGeo.algorithms.AggregateFeatures as af
import CaGeo.algorithms.BasicFeatures as bf
import CaGeo.algorithms.SegmentFeatures as sf
import numpy as np
import pycatch22
from joblib import Parallel, delayed
from joblib import effective_n_jobs
from sklearn.base import BaseEstimator, ClassifierMixin
from sklearn.ensemble import RandomForestClassifier
from tqdm.auto import tqdm


class T_CIF(BaseEstimator, ClassifierMixin, ABC):
    # interval types: {None: [a:b] or [0] if a > len(trj), percentage: percentage, reverse_fill: if a | b > len(trj),
    # reverse trj}
    def __init__(self, n_trees, n_interval, min_length, max_length, interval_type=None, accurate=False,
                 use_cageo=True, use_catch22=False, lat_lon=False, seed=42, n_jobs=24, verbose=False):

        if min_length > max_length:
            raise ValueError(f"min_length must be less then max_length. Values: (min={min_length}, max={max_length})")
        if not use_cageo and not use_catch22:
            raise ValueError("One of 'use_cageo' or 'use_catch22' must be True")

        self.intervals = []
        self.n_trees = n_trees
        self.n_interval = n_interval
        self.min_length = min_length
        self.max_length = max_length
        self.interval_type = interval_type
        self.accurate = accurate
        self.use_catch22 = use_catch22
        self.use_cageo = use_cageo
        self.lat_lon = lat_lon
        self.n_jobs = n_jobs
        self.seed = seed
        self.verbose = verbose

        self.starts = None
        self.stops = None
        self.X = None
        self.clf = None

        self.clf = RandomForestClassifier(n_estimators=self.n_trees, max_depth=10, bootstrap=False,
                                          random_state=self.seed, n_jobs=self.n_jobs)

    @abstractmethod
    def generate_intervals(self):
        pass

    @abstractmethod
    def get_subset(self, X_row, start, stop):
        pass

    def _chunkize(self, X, n_chunks):
        chunk_size = max(math.floor(len(X) / n_chunks), 1)

        for i in range(0, len(X), chunk_size):
            yield deepcopy(X[i:i + chunk_size])

    def dividi(self, n_tr, n_chunks):
        chunk_size = max(math.floor(n_tr / n_chunks), 1)

        divisi = []
        for i in range(0, n_tr, chunk_size):
            divisi.append((i, i + chunk_size))

        return divisi

    #@profile
    def transform(self, X):
        if len(X[0]) == 3 and not self.use_cageo and self.use_catch22:
            raise Exception("Model is set to use only catch22 features, but only latitude, longitude, and time were "
                            "provided")

        self.X = X

        if self.starts is None:
            self.starts, self.stops = self.generate_intervals()

        features = []

        chunk_size = max(math.floor(len(X) / (self.n_jobs * 10)), 1)

        X_chunk_list = []
        for i in range(0, len(X), chunk_size):
            X_chunk_list.append(deepcopy(X[i:i + chunk_size]))

        estimators = Parallel(n_jobs=self.n_jobs, verbose=self.verbose, prefer="processes")(
            delayed(_transform_inner_loop)(X_chunk, self.starts, self.stops, str(type(self)), self.min_length,
                                           self.interval_type, self.accurate, self.use_cageo, self.use_catch22,
                                           self.lat_lon)
            for i, X_chunk in enumerate(X_chunk_list))

        for res in tqdm(estimators, desc="collecting results", position=0, leave=False, disable=not self.verbose):
            features.append(res)

        return np.concatenate(features)

    def fit(self, X, y):  # list of tuples (time, lat, lon, others1, ...)
        if len(X[0]) == 3 and not self.use_cageo and self.use_catch22:
            raise Exception("Model is set to use only catch22 features, but only latitude, longitude, and time were "
                            "provided")
        self.X = X

        if self.starts is None:
            self.starts, self.stops = self.generate_intervals()


        self.clf.fit(self.transform(X), y)

        return self

    def get_col_names(self, additional_signal_feat_name=[]):
        catch22_feat = [
            'mode-5', 'mode-10', 'acf-timescale', 'acf-first-min', 'ami2', 'trev', 'high-fluctuation',
            'stretch-high', 'transition-matrix', 'periodicity', 'embedding-dist', 'ami-timescale',
            'whiten-timescale', 'outlier-timing_pos', 'outlier-timing-neg', 'centroid-freq', 'stretch-decreasing',
            'entropy-pairs', 'rs-range', 'dfa', 'low-freq-power', 'forecast-error', "mean", "SD"
        ]

        final_features = []
        for i in range(len(self.starts)):
            if self.use_cageo:
                base_features = ["speed", "dist", "direction", "turningAngles", "acceleration", "acceleration2"]
                if self.lat_lon:
                    base_features += additional_signal_feat_name[:3]

                for base_feature in base_features:
                    for aggragate_feature in ["sum", "std", "max", "min", "cov", "var", "mean", "rate-b", "rate-u"]:
                        final_features.append(f"{aggragate_feature}({base_feature}_{i})")

                final_features += [f"straightness_{i}", f"meanSquaredDisplacement_{i}", f"intensityUse_{i}",
                                   f"sinuosity_{i}"]

            if self.use_catch22:
                for signal_name in additional_signal_feat_name[3:]:
                    final_features += [f"{catch22_feat_name}_{i}({signal_name})" for catch22_feat_name in catch22_feat]

        return final_features

    def predict(self, X):
        return self.clf.predict(self.transform(X))

    @abstractmethod
    def print_sections(self):
        pass


#@profile
def _transform_inner_loop(X_list, starts, stops, tipo, min_length, interval_type, accurate, use_cageo, use_catch22,
                          lat_lon):
    verbose = False

    if not verbose:
        warnings.filterwarnings('ignore')

    n_base = 6
    n_base += 3 if lat_lon else 0

    n_feat_cageo = n_base * 9 + 4 if use_cageo else 0
    n_feat_catch22 = 24 * len(X_list[0][3:]) if use_catch22 else 0

    features = np.zeros((len(X_list), (n_feat_cageo+n_feat_catch22) * len(starts))) * np.nan

    for i, X in enumerate(X_list):
        if "time" in tipo:
            from TCIF.classes.T_CIF_time import T_CIF_time
            get_subset = T_CIF_time(None, None, min_length, interval_type=interval_type).get_subset
        elif "space" in tipo:
            from TCIF.classes.T_CIF_space import T_CIF_space
            get_subset = T_CIF_space(None, None, min_length, interval_type=interval_type).get_subset
        else:
            from TCIF.classes.T_CIF_observation import T_CIF_observations
            get_subset = T_CIF_observations(None, None, min_length, interval_type=interval_type).get_subset

        feature = []
        it = tqdm(list(zip(starts, stops)), disable=not verbose, desc="Processing interval", leave=False, position=0)
        for start, stop in it:
            X_sub = get_subset(X, start, stop)

            if use_cageo:
                it.set_description("Computing kinematic features")
                X_time_sub, X_lat_sub, X_lon_sub = X_sub[:3]

                dist = np.nan_to_num(bf.distance(X_lat_sub, X_lon_sub, accurate=accurate))

                transformed = [
                    np.nan_to_num(bf.speed(X_lat_sub, X_lon_sub, X_time_sub, accurate=dist[1:])),
                    dist,
                    np.nan_to_num(bf.direction(X_lat_sub, X_lon_sub)),
                    np.nan_to_num(bf.turningAngles(X_lat_sub, X_lon_sub)),
                    np.nan_to_num(bf.acceleration(X_lat_sub, X_lon_sub, X_time_sub, accurate=dist[1:])),
                    np.nan_to_num(bf.acceleration2(X_lat_sub, X_lon_sub, X_time_sub, accurate=dist[1:]))
                ]

                if lat_lon:
                    transformed += [X_lat_sub, X_lon_sub, X_time_sub]

                for arr in tqdm(transformed, disable=not verbose, desc="computing aggregate features",
                                leave=False, position=1):
                    for f in [af.sum, af.std, af.max, af.min, af.cov, af.var]:
                        feature.append(f(arr, None))
                    feature.append(np.array([arr.mean()]))  # mean
                    feature.append(af.rate_below(arr, arr.mean() * .25, None))
                    feature.append(af.rate_upper(arr, arr.mean() * .75, None))

                del transformed[:]
                feature.append([np.nan_to_num(sf.straightness(X_lat_sub, X_lon_sub))])
                feature.append([np.nan_to_num(sf.meanSquaredDisplacement(X_lat_sub, X_lon_sub))])
                feature.append([np.nan_to_num(sf.intensityUse(X_lat_sub, X_lon_sub))])
                feature.append([np.nan_to_num(sf.sinuosity(X_lat_sub, X_lon_sub))])

            if use_catch22:
                it.set_description(
                    f"Comupting catch22 features for {len(X[3:])} signals of len {0 if len(X[3:]) == 0 else len(X_sub[3])}")
                for X_other in X_sub[3:]:
                    _, values = pycatch22.catch22_all(X_other, catch24=True).values()
                    values = np.nan_to_num(values)
                    feature += values.reshape(-1, 1).tolist()

        for f in feature:
            if len(f) == 0:
                print("HERE")
            if np.isnan(f[0]).all() or not np.isfinite(f[0]).all():
                print("HERE")

        #features.append(feature)
        if features[i].shape != np.array(feature).T.reshape(-1).shape:
            print("HERE")
        features[i] = np.array(feature).T.reshape(-1)
        del feature

    return features


def _joblib_parallel_args(**kwargs):
    import joblib

    if joblib.__version__ >= LooseVersion('0.12'):
        return kwargs

    extra_args = set(kwargs.keys()).difference({'prefer', 'require'})
    if extra_args:
        raise NotImplementedError('unhandled arguments %s with joblib %s'
                                  % (list(extra_args), joblib.__version__))
        args = {}
        if 'prefer' in kwargs:
            prefer = kwargs['prefer']
        if prefer not in ['threads', 'processes', None]:
            raise ValueError('prefer=%s is not supported' % prefer)
        args['backend'] = {'threads': 'threading',
                           'processes': 'multiprocessing',
                           None: None}[prefer]

        if 'require' in kwargs:
            require = kwargs['require']
        if require not in [None, 'sharedmem']:
            raise ValueError('require=%s is not supported' % require)
        if require == 'sharedmem':
            args['backend'] = 'threading'
        return args


def _partition_estimators(n_estimators, n_jobs):
    # Compute the number of jobs
    n_jobs = min(effective_n_jobs(n_jobs), n_estimators)

    # Partition estimators between jobs
    n_estimators_per_job = np.full(n_jobs, n_estimators // n_jobs, dtype=np.int)
    n_estimators_per_job[:n_estimators % n_jobs] += 1
    starts = np.cumsum(n_estimators_per_job)

    return n_jobs, n_estimators_per_job.tolist(), [0] + starts.tolist()
