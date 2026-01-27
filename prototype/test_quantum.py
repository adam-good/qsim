import unittest
import numpy as np
from prototype.quantum.gate import HGate, CNOTGate
from prototype.quantum.qubit import Qubit, QuantumState

class TestHGate(unittest.TestCase):
    def test_h_gate(self):
        h_gate = HGate()
        qubits = np.array([1.0, 0.0])
        result = h_gate(qubits)
        expected_result = np.array([1/np.sqrt(2), 1/np.sqrt(2)])
        np.testing.assert_almost_equal(result, expected_result)

class TestCNOTGate(unittest.TestCase):
    def test_cnot_gate(self):
        cnot_gate = CNOTGate()
        qubits = np.array([1.0, 0.0, 0.0, 0.0])
        result = cnot_gate(qubits)
        expected_result = np.array([1.0, 0.0, 0.0, 0.0])
        np.testing.assert_almost_equal(result, expected_result)

class TestQubit(unittest.TestCase):
    def test_qubit_measure(self):
        qubit = Qubit()
        outcome = qubit.measure()
        self.assertIn(outcome, [0, 1])

if __name__ == "__main__":
    unittest.main()
