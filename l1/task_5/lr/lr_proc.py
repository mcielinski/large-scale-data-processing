from typing import List
import concurrent.futures

from lr import base

NUM_OF_PROCESSES = 8


def list_to_chunks(list_, num_chunks=NUM_OF_PROCESSES):
    # split list into n chunks
    l_len = len(list_)
    chunks = []
    el_per_chunk = l_len // num_chunks

    for i in range(num_chunks):
        next_i = i + 1
        first = i * el_per_chunk
        last = next_i * el_per_chunk if next_i != num_chunks else l_len
        chunks.append(list_[first:last])

    return chunks


def get_mean(list_, data_size):
    l_sum = 0
    for i in range(len(list_)):
        l_sum += list_[i]

    return l_sum / data_size


def get_SS(X, y, X_mean, y_meam):
    SS_xy = SS_xx = 0
    for i in range(len(X)):
        X_diff = X[i] - X_mean
        y_diff = y[i] - y_meam
        SS_xy += X_diff * y_diff
        SS_xx += X_diff * X_diff

    return SS_xy, SS_xx


class LinearRegressionProcess(base.LinearRegression):
    def fit(self, X: List[float], y: List[float]) -> base.LinearRegression:

        data_len = len(X)
        X_chunks = list_to_chunks(X)
        y_chunks = list_to_chunks(y)

        with concurrent.futures.ProcessPoolExecutor(
                max_workers=NUM_OF_PROCESSES) as executor:
            X_mean = 0
            y_mean = 0
            for i in range(len(X_chunks)):
                X_mean += executor.submit(get_mean, X_chunks[i], data_len)\
                    .result()
                y_mean += executor.submit(get_mean, y_chunks[i], data_len)\
                    .result()

            SS_list = []
            for i in range(len(X_chunks)):
                SS_list.append(executor.submit(get_SS, X_chunks[i], y_chunks[i],
                                               X_mean, y_mean).result())

            SS_xy = SS_xx = 0
            for i in range(len(SS_list)):
                SS_xy += SS_list[i][0]
                SS_xx += SS_list[i][1]

            b_1 = SS_xy / SS_xx
            b_0 = y_mean - b_1 * X_mean

            self._coef = [b_0, b_1]

            return self
