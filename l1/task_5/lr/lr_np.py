from typing import List
import numpy as np

from lr import base


class LinearRegressionNumpy(base.LinearRegression):
    def fit(self, X: List[float], y: List[float]) -> base.LinearRegression:

        X_ = np.array(X)
        y_ = np.array(y)
        X_mean = np.mean(X_)
        y_mean = np.mean(y_)

        X_diff = X_ - X_mean
        y_diff = y_ - y_mean

        SS_xy = np.sum(X_diff * y_diff)
        SS_xx = np.sum(X_diff * X_diff)
        b_1 = SS_xy / SS_xx
        b_0 = y_mean - b_1 * X_mean

        self._coef = [b_0, b_1]

        return self
