import os
import random

import numpy as np

from TCIF.classes.T_CIF import T_CIF


class T_CIF_time(T_CIF):

    def __init__(self, n_trees, n_interval, min_length, max_length=np.inf, interval_type="percentage", accurate=False,
                 use_cageo=True, use_catch22=False, lat_lon=False, n_jobs=1, seed=42, verbose=False):
        super().__init__(
            n_trees=n_trees,
            n_interval=n_interval,
            min_length=min_length,
            max_length=max_length,
            interval_type=interval_type,
            n_jobs=n_jobs,
            seed=seed,
            verbose=verbose,
            accurate=accurate,
            use_catch22=use_catch22,
            use_cageo=use_cageo,
            lat_lon=lat_lon
        )

        self.min_t = None
        self.max_t = None

        if verbose:
            print(f"{interval_type}, min:{min_length}, max:{max_length}", flush=True)

        if interval_type is None or interval_type in ["reverse_fill", "fill"]:
            if type(min_length) != int or (type(max_length) != int and max_length != np.inf):
                raise ValueError(f"min_length={type(min_length)} and max_length={type(min_length)} unsupported when "
                                 f"interval_type={interval_type}. Please use min_length=int and None=[int or inf]")

        elif interval_type == "percentage":
            if type(min_length) != float or type(max_length) != float:
                raise ValueError(f"min_length={type(min_length)} and max_length={type(min_length)} unsupported when "
                                 f"interval_type={interval_type}. Please use min_length=float and None=[float or inf]")

        else:
            raise ValueError(f"interval_type={interval_type} unsupported. supported interval types: [None, percentage, "
                             f"reverse_fill]")

        self.interval_type = interval_type

    def generate_intervals(self):
        random.seed(self.seed)

        self.max_t = int(max([max(x[0]) for x in self.X]))
        self.min_t = int(min([min(x[0]) for x in self.X]))

        if self.interval_type in [None, "reverse_fill", "fill"]:
            starting_p = random.sample(range(self.min_t, self.max_t - self.min_length), self.n_interval)
            ending_p = []
            for p in starting_p:
                l = random.randint(self.min_length, self.max_t - p) + p

                ending_p.append(l)

            return starting_p, ending_p

        elif self.interval_type == "percentage":
            starting_p = [random.uniform(0.0, 1.0 - self.min_length) for _ in range(self.n_interval)]

            ending_p = []
            for p in starting_p:
                l = random.uniform(self.min_length, min(1.0 - p, self.max_length)) + p

                ending_p.append(l)

            return starting_p, ending_p

    def get_subset(self, X_row, start, stop):
        if self.interval_type in [None, "percentage"]:
            return self._get_subset_none_perc(X_row, start, stop)

        elif self.interval_type == "reverse_fill":
            return self._get_subset_reverse_fill(X_row, start, stop)

        elif self.interval_type == "fill":
            return self._get_subset_fill(X_row, start, stop)

    def _get_subset_none_perc(self, X_row, start, stop):
        if self.interval_type == "percentage":
            X_row_min_t = min(X_row[0])
            X_row_max_t = max(X_row[0])
            start = (X_row_max_t - X_row_min_t) * start + X_row_min_t
            stop = (X_row_max_t - X_row_min_t) * stop + X_row_min_t

        start_idx = None
        stop_idx = None

        for idx, time in enumerate(X_row[0]):
            if time >= start and start_idx is None:
                start_idx = idx

            if time >= stop:
                stop_idx = idx
                break

        if start_idx is None:
            return tuple([x[0:1] for x in X_row])
        elif stop_idx is None:
            return tuple([x[start_idx:] for x in X_row])
        elif start_idx == stop_idx:
            return tuple([x[start_idx:stop_idx + 1] for x in X_row])
        else:
            return tuple([x[start_idx:stop_idx] for x in X_row])

    def _get_subset_reverse_fill(self, X_row, start, stop):
        return_value = tuple([[] for _ in range(len(X_row))])
        X_row_clone = X_row

        subsequence_time = 0

        while subsequence_time < stop or len(return_value[0]) == 0:
            # special case: at least 1 element -> in the case that delta_time > stop-start
            for it, (time, time_prec) in enumerate(zip(X_row_clone[0], [None] + X_row_clone[0][:-1].tolist())):

                if subsequence_time < start:
                    if time_prec is not None:
                        subsequence_time += abs(time_prec - time)
                    continue

                if subsequence_time != 0 and it == 0:  # 1st element after a flip -> skip to avoid duplicates
                    continue

                if len(return_value[0]) == 0:
                    return_value[0].append(time)
                else:
                    return_value[0].append(return_value[0][len(return_value[0]) - 1] + abs(time_prec - time))
                    subsequence_time += abs(time_prec - time)

                for i in range(1, len(return_value)):
                    return_value[i].append(X_row_clone[i][it])

                if subsequence_time >= stop and len(return_value[0]) > 0:
                    # special case: at least 1 element -> in the case that delta_time > stop-start
                    break

            X_row_clone = tuple([np.flip(X_row_clone[i]) for i in range(len(X_row))])

        if len(return_value[0]) == 0:
            raise Exception("len(return_value[0]) == 0")

        return tuple([np.array(return_value_i) for return_value_i in return_value])

    def _get_subset_fill(self, X_row, start, stop):
        X_row_clone = X_row

        base = tuple([X_row_clone[i][0] for i in range(len(X_row_clone))])
        return_value = tuple([[base_feat] for base_feat in base])
        X_row_clone = tuple([X_row_clone[i][1:] - base[i] for i in range(len(base))])

        subsequence_time = 0

        while subsequence_time < stop or len(return_value[0]) == 0:
            # special case: at least 1 element -> in the case that delta_time > stop-start
            for it, (lat, lon, time, time_prec) in enumerate(zip(X_row_clone[0],
                                                                 X_row_clone[1],
                                                                 X_row_clone[2],
                                                                 X_row_clone[2])):

                for i in range(len(return_value)):
                    return_value[i].append(base[i]+X_row_clone[i][it]+X_row_clone[i][-1] * (len(return_value[i]) // len(return_value[0])))

                subsequence_time += time + return_value[0][-1]

                if subsequence_time >= stop and len(return_value[0]) > 0:
                    # special case: at least 1 element -> in the case that delta_time > stop-start
                    break

        return tuple([np.array(return_value_i) for return_value_i in return_value])

    def print_sections(self):
        if self.interval_type in [None, "reverse_fill"]:
            width = os.get_terminal_size().columns

            c = width / (self.max_t - self.min_t)

            print("".join(["#" for _ in range(width)]))

            for start, stop in zip(self.starts, self.stops):

                to_print = [" " for _ in range(int((start - self.min_t) * c))]

                to_print += ["-" for _ in range(int((start - self.min_t) * c), int((stop - self.min_t) * c))]

                print("".join(to_print))
        else:
            raise Exception("Unimplemented")
