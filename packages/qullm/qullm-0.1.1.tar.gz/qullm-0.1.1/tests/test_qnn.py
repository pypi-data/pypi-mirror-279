# tests/test_qnn.py

import unittest
from qullm.qnn import QuantumNeuralNetwork

class TestQuantumNeuralNetwork(unittest.TestCase):
    def test_simulate(self):
        qnn = QuantumNeuralNetwork()
        result = qnn.simulate("test input")
        self.assertEqual(result, "Simulated output for input: test input")

if __name__ == '__main__':
    unittest.main()