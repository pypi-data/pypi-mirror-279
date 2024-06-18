# tests/test_neural_network.py
import unittest
import numpy as np
from zyro_py.dl.neural_network import NeuralNetwork
from zyro_py.dl.layers import Dense, Activation

class TestNeuralNetwork(unittest.TestCase):
    def test_forward_pass(self):
        model = NeuralNetwork()
        model.add(Dense(2, 3))
        model.add(Activation('relu'))
        model.add(Dense(3, 1))
        X = np.array([[1, 2], [3, 4], [5, 6]])
        output = model.forward(X)
        self.assertEqual(output.shape, (3, 1))

if __name__ == '__main__':
    unittest.main()
