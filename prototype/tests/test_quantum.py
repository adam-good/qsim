from numpy.ma.testutils import assert_equal
import unittest
import numpy as np
from quantum.gate import HGate, XGate
from quantum.qubit import Qubit, QuantumState

class TestHGate(unittest.TestCase):
    def test_h_gate(self):
        h_gate = HGate()
        qubit = Qubit()
        result = h_gate(qubit)
        expected_result = np.array([1, 1]) / np.sqrt(2)
        np.testing.assert_almost_equal(result, expected_result)

class TestXGate(unittest.TestCase):
    def test_cnot_gate(self):
        cnot_gate = XGate()
        qubits = Qubit()
        result = cnot_gate(qubits)
        expected_result = np.array([0.0, 1.0])
        np.testing.assert_almost_equal(result, expected_result)

class TestQuantumState(unittest.TestCase):
    def test_quantumstate_to_vector(self):
        vec = np.array([np.pi, 2*np.pi])
        state = QuantumState(vec)
        outcome = state.vector
        np.testing.assert_array_equal(outcome, vec)

    def test_quantumestate_angles(self):
        h = 1.0 / np.sqrt(2) # hadamard value
        vectors = [
            np.array([1.0, 0.0]),    # ket 0
            np.array([0.0, 1.0]),    # ket 1
            np.array([h, h]),        # ket plus
            np.array([h, -h]),       # key minus
            
        ]
        targets = [0.0, 90.0, 45.0, 315.0]
        for vec, target in zip(vectors, targets):
            psi = QuantumState(vec)
            outcome = psi.angle
            np.testing.assert_equal(outcome, target)
      

    def test_quantumstate_bloch_angles(self):
        h = 1.0 / np.sqrt(2) # hadamard value
        vectors = [
            np.array([1.0, 0.0]),    # ket 0
            np.array([0.0, 1.0]),    # ket 1
            np.array([h, h]),        # ket plus
            np.array([h, -h]),       # key minus
            
        ]
        targets = (0.0, 180.0, 90.0, 270.0)
        for vec, target in zip(vectors, targets):
            psi = QuantumState(vec)
            outcome = psi.bloch_angle
            np.testing.assert_equal(outcome, target)

    def test_quantumstate_probability_distribution(self):
        h = 1.0 / np.sqrt(2) # hadamard value
        vectors = [
            np.array([1.0, 0.0]),    # ket 0
            np.array([0.0, 1.0]),    # ket 1
            np.array([h, h]),        # ket plus
            np.array([h, -h]),       # key minus
        ]
        targets = [
            [1.0, 0.0],
            [0.0, 1.0],
            [0.5, 0.5],
            [0.5, 0.5]
        ]
        for vec, target in zip(vectors, targets):
            psi = QuantumState(vec)
            outcome = psi.probability_distribution
            np.testing.assert_array_almost_equal(outcome, target)

    def test_quantumstate_eq(self):
        psi = QuantumState(np.array([1.0,0.0]))
        omega = QuantumState(np.array([1.0,0.0]))
        assert_equal(psi == omega, True)

class TestQubit(unittest.TestCase):
  
    def test_qubit_measure(self):
        target = QuantumState(np.array([1,0]))
        ket0 = Qubit(target)
        outcome = ket0.measure()
        np.testing.assert_array_almost_equal(outcome.state_vec, target.state_vec)

        target = QuantumState(np.array([0,1]))
        ket1 = Qubit(target)
        outcome = ket1.measure()
        np.testing.assert_array_almost_equal(outcome.state_vec, target.state_vec)

    def test_qubit_eq(self):
        x_state = QuantumState(np.array([1.0, 0.0]))
        y_state = QuantumState(np.array([1.0, 0.0]))
        x = Qubit(x_state)
        y = Qubit(y_state)
        assert_equal(x == y, True)

if __name__ == "__main__":
    unittest.main()
