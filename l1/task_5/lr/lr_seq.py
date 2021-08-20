from typing import List

from lr import base


class LinearRegressionSequential(base.LinearRegression):
    def fit(self, X: List[float], y: List[float]) -> base.LinearRegression:
        # http://www.cs.uni.edu/~campbell/stat/reg.html

        X_sum = y_sum = 0
        data_len = len(X)

        for i in range(data_len):
            X_sum += X[i]
            y_sum += y[i]
        X_mean = X_sum / data_len
        y_mean = y_sum / data_len

        SS_xy = SS_xx = 0

        for i in range(data_len):
            X_diff = X[i] - X_mean
            y_diff = y[i] - y_mean
            SS_xy += X_diff * y_diff
            SS_xx += X_diff * X_diff
        b_1 = SS_xy / SS_xx
        b_0 = y_mean - b_1 * X_mean

        self._coef = [b_0, b_1]

        return self
