import unittest

import numpy as np

import lr


class TestLinearRegression(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._x = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        self._y = [1, 3, 2, 5, 7, 8, 8, 9, 10, 12]

    def _assert_params(self, model):
        b = model._coef
        self.assertAlmostEqual(b[0], 1.2363636363636363)
        self.assertAlmostEqual(b[1], 1.1696969696969697)

    def _assert_error(self, model):
        y_pred = model.predict(self._x)
        err = np.sum((np.array(self._y) - y_pred) ** 2)
        self.assertAlmostEqual(err, 5.624242424242423)

    def _test_lr(self, model_cls):
        model = model_cls()
        model.fit(self._x, self._y)
        
        self._assert_params(model)
        self._assert_error(model)

    def test_seq_impl(self):
        self._test_lr(lr.LinearRegressionSequential)

    def test_numpy_impl(self):
        self._test_lr(lr.LinearRegressionNumpy)

    def test_threads_impl(self):
        self._test_lr(lr.LinearRegressionThreads)

    def test_proc_impl(self):
        self._test_lr(lr.LinearRegressionProcess)


if __name__ == '__main__':
    unittest.main()

