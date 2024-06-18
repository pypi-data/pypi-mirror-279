# tests/test_logistic_regression.py
import unittest
import numpy as np
from zyro_py.ml.logistic_regression import LogisticRegression

class TestLogisticRegression(unittest.TestCase):
    def test_fit(self):
        X = np.array([[1, 1], [1, 2], [2, 2], [2, 3]])
        y = np.array([0, 0, 1, 1])
        model = LogisticRegression()
        model.fit(X, y)
        predictions = model.predict(X)
        self.assertEqual(list(predictions), list(y))

    def test_predict(self):
        X = np.array([[1, 1], [1, 2], [2, 2], [2, 3]])
        y = np.array([0, 0, 1, 1])
        model = LogisticRegression()
        model.fit(X, y)
        predictions = model.predict(X)
        for pred, true in zip(predictions, y):
            self.assertEqual(pred, true)

if __name__ == '__main__':
    unittest.main()
