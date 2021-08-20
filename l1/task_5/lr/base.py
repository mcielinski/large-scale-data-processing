from __future__ import annotations

import abc
from typing import List

import numpy as np


class ScikitPredictor(abc.ABC):
    @abc.abstractmethod
    def fit(self, X, y):
        pass

    @abc.abstractmethod
    def predict(self, X):
        pass


class LinearRegression(ScikitPredictor):
    def __init__(self):
        self._coef = None

    @abc.abstractmethod
    def fit(self, X: List[float], y: List[float]) -> LinearRegression:
        pass

    def predict(self, X: List[float]) -> np.ndarray:
        if self._coef is None:
            raise RuntimeError('Please fit model before prediction')

        return self._coef[0] + self._coef[1] * np.array(X)
