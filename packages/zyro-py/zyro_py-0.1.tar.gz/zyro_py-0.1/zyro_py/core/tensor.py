# tests/test_tensor.py
import unittest
from zyro_py.core.tensor import Tensor

class TestTensor(unittest.TestCase):
    def test_addition(self):
        t1 = Tensor([1, 2, 3])
        t2 = Tensor([4, 5, 6])
        result = t1 + t2
        expected = Tensor([5, 7, 9])
        self.assertEqual(result.data.tolist(), expected.data.tolist())

    def test_subtraction(self):
        t1 = Tensor([4, 5, 6])
        t2 = Tensor([1, 2, 3])
        result = t1 - t2
        expected = Tensor([3, 3, 3])
        self.assertEqual(result.data.tolist(), expected.data.tolist())

    def test_multiplication(self):
        t1 = Tensor([1, 2, 3])
        t2 = Tensor([4, 5, 6])
        result = t1 * t2
        expected = Tensor([4, 10, 18])
        self.assertEqual(result.data.tolist(), expected.data.tolist())

if __name__ == '__main__':
    unittest.main()
