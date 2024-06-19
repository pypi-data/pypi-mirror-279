import os
import random

import numpy as np

from TCIF.classes.T_CIF import T_CIF


class T_CIF_observations(T_CIF):

    # interval types: {None: [a:b] or [0] if a > len(trj), percentage: percentage, reverse_fill: if a | b > len(trj),
    # reverse trj}
    def __init__(self, n_trees, n_interval, min_length, max_length=np.inf, interval_type=None, accurate=False,
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

        if self.interval_type in [None, "reverse_fill", "fill"]:
            max_len = max([len(x[0]) for x in self.X])

            starting_p = random.sample(range(0, max_len - self.min_length), self.n_interval)
            ending_p = []
            for p in starting_p:
                l = random.randint(self.min_length, min(max_len - p, self.max_length)) + p

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
        if self.interval_type is None:
            return self._get_subset_none(X_row, start, stop)

        elif self.interval_type == "percentage":
            return self._get_subset_percentage(X_row, start, stop)

        elif self.interval_type == "reverse_fill":
            return self._get_subset_reverse_fill(X_row, start, stop)

        elif self.interval_type == "fill":
            return self._get_subset_fill(X_row, start, stop)

    def _get_subset_none(self, X_row, start, stop):
        return_value = tuple([x[start:min(stop, len(x))] for x in X_row])

        if len(return_value[0]) == 0:  # special case: start > len(trajectory)
            return_value = [X_row[i][-1:] for i in range(len(X_row))]

        return return_value

    def _get_subset_percentage(self, X_row, start, stop):
        length = len(X_row[0])
        start = int(length * start)
        stop = int(length * stop)

        if start == stop:
            stop += 1

        return tuple([x[start:stop] for x in X_row])

    def _get_subset_reverse_fill(self, X_row, start, stop):
        interval_len = stop - start
        return_value = tuple([np.ones(interval_len)*np.nan for _ in range(len(X_row))])
        X_row_clone = X_row

        count = min(stop, len(X_row[0])) - start

        if count >= 0:
            for i in range(len(X_row)):
                return_value[i][:count] = X_row[i][start:min(stop, len(X_row[0]))]

        while count != interval_len:
            X_row_clone = tuple([np.flip(X_row_clone[i]) for i in range(len(X_row))])
            for i, (time, time_prec) in enumerate(zip(X_row_clone[0][1:], X_row_clone[0][:-1])):
                if count < 0:
                    count += 1
                    continue

                return_value[0][count] = return_value[0][count - 1] + abs(time_prec - time)
                for j in range(1, len(X_row)):
                    return_value[j][count] = X_row_clone[j][i]

                count += 1
                if count == interval_len:
                    break
        return return_value

    def _get_subset_fill(self, X_row, start, stop):
        interval_len = stop - start

        subset = tuple([x[start:min(stop, len(x))] for x in X_row])

        if len(subset[0]) < 2:  # special case: start > len(trajectory)
            return tuple([X_row[i][-1:] for i in range(len(X_row))])

        base = tuple([subset[i][0] for i in range(len(subset))])

        offsets = tuple([subset[i] - base[i] for i in range(len(subset))])

        return_value = tuple([np.ones(interval_len)*np.nan for _ in range(len(X_row))])

        for i in range(interval_len):
            for j in range(len(X_row)): #per ogni segnale
                if len(subset[0]) == 0:
                    raise Exception("len(subset[0]) == 0")
                return_value[j][i] = base[j] + offsets[j][i % len(subset[0])] + offsets[j][-1] * (i // len(offsets[0]))

        return return_value


    def print_sections(self):
        width = os.get_terminal_size().columns

        max_w = max([len(x[0]) for x in self.X])

        c = width / max_w

        print("".join(["#" for _ in range(width)]))

        for start, stop in zip(self.starts, self.stops):
            to_print = []

            if self.interval_type in [None, "reverse_fill"]:
                to_print = [" " for _ in range(int(start * c))]

                to_print += ["-" for _ in range(int(start * c), int(stop * c))]

            if self.interval_type == "percentage":
                to_print = [" " for _ in range(int(start * width))]

                to_print += ["-" for _ in range(int(start * width), int(stop * width))]

            print("".join(to_print))
