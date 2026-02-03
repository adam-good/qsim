import unittest
import numpy as np
#from quantum.gate import HGate, CNOTGate
from quantum.qubit import Qubit, QuantumState

# class TestHGate(unittest.TestCase):
#     def test_h_gate(self):
#         h_gate = HGate()
#         qubits = np.array([1.0, 0.0])
#         result = h_gate(qubits)
#         expected_result = np.array([1/np.sqrt(2), 1/np.sqrt(2)])
#         np.testing.assert_almost_equal(result, expected_result)

# class TestCNOTGate(unittest.TestCase):
#     def test_cnot_gate(self):
#         cnot_gate = CNOTGate()
#         qubits = np.array([1.0, 0.0, 0.0, 0.0])
#         result = cnot_gate(qubits)
#         expected_result = np.array([1.0, 0.0, 0.0, 0.0])
#         np.testing.assert_almost_equal(result, expected_result)

class TestQuantumState(unittest.TestCase):
    def test_quantumstate_to_vector(self):
        vec = np.array([np.pi, 2*np.pi])
        state = QuantumState(vec)
        outcome = state.to_vector()
        np.testing.assert_array_equal(outcome, vec)

    def test_quantumestate_angles(self):
        ket0 = QuantumState(np.array([1.0, 0.0]))
        outcome = ket0.to_angles()
        target = 0.0
        np.testing.assert_equal(outcome, target)

        ket1 = QuantumState(np.array([0.0, 1.0]))
        outcome = ket1.to_angles()
        target = 90.0
        np.testing.assert_equal(outcome, target)

        ket_plus = QuantumState(np.array([1.0, 1.0]) / np.sqrt(2))
        outcome = ket_plus.to_angles()
        target = 45.0
        np.testing.assert_equal(outcome, target)

        ket_minus = QuantumState(np.array([1.0, -1.0]) / np.sqrt(2))
        outcome = ket_minus.to_angles()
        target = 360.0 - 45.0
        np.testing.assert_equal(outcome, target)

    def test_quantumstate_bloch_angles(self):
        ket0 = QuantumState(np.array([1.0, 0.0]))
        outcome = ket0.to_bloch_angles()
        target = 0.0
        np.testing.assert_equal(outcome, target)

        ket1 = QuantumState(np.array([0.0, 1.0]))
        outcome = ket1.to_bloch_angles()
        target = 180.0
        np.testing.assert_equal(outcome, target)

        ket_plus = QuantumState(np.array([1.0, 1.0]) / np.sqrt(2))
        outcome = ket_plus.to_bloch_angles()
        target = 90.0
        np.testing.assert_equal(outcome, target)

        ket_minus = QuantumState(np.array([1.0, -1.0]) / np.sqrt(2))
        outcome = ket_minus.to_bloch_angles()
        target = 270
        np.testing.assert_equal(outcome, target)

# class TestQubit(unittest.TestCase):
  
#     def test_qubit_measure(self):
#         qubit = Qubit()
#         outcome = qubit.measure()
#         self.assertIn(outcome, [0, 1])

if __name__ == "__main__":
    unittest.main()
