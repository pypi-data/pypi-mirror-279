# tests/test_linear_regression.py
import unittest
import numpy as np
from zyro_py.ml.linear_regression import LinearRegression

class TestLinearRegression(unittest.TestCase):
    def test_fit(self):
        X = np.array([[1, 1], [1, 2], [2, 2], [2, 3]])
        y = np.dot(X, np.array([1, 2])) + 3
        model = LinearRegression()
        model.fit(X, y)
        self.assertAlmostEqual(model.weights[0], 1, places=1)
        self.assertAlmostEqual(model.weights[1], 2, places=1)
        self.assertAlmostEqual(model.bias, 3, places=1)

    def test_predict(self):
        X = np.array([[1, 1], [1, 2], [2, 2], [2, 3]])
        y = np.dot(X, np.array([1, 2])) + 3
        model = LinearRegression()
        model.fit(X, y)
        predictions = model.predict(X)
        for pred, true in zip(predictions, y):
            self.assertAlmostEqual(pred, true, places=1)

if __name__ == '__main__':
    unittest.main()
