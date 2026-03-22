from utils.typing import Vector
import unittest
import numpy as np
import quantum.gate as qgate
import quantum.state as qstate

class TestGates(unittest.TestCase):
    def test_h_gate(self):
        qubit = qstate.KET0
        result = qgate.hadamard(qubit)
        target = qstate.QState((1, 1)) / np.sqrt(2)
        self.assertEqual(result, target)

    def test_x_gate(self):
        qubit = qstate.KET0
        result = qgate.xgate(qubit)
        target = qstate.QState((0,1))
        self.assertEqual(result, target)

class TestQuantumState(unittest.TestCase):
    def test_quantumestate_angles(self):
        h = 1.0 / np.sqrt(2) # hadamard value
        qubits = [
           qstate.QState((1.0, 0.0)),    # ket 0
           qstate.QState((0.0, 1.0)),    # ket 1
           qstate.QState((h, h)),        # ket plus
           qstate.QState((h, -h)),       # key minus
            
        ]
        targets = [0.0, 90.0, 45.0, 315.0]
        for psi, target in zip(qubits, targets):
            outcome = qstate.angle(psi)
            np.testing.assert_equal(outcome, target)

    def test_quantumstate_bloch_angles(self):
        h = 1.0 / np.sqrt(2) # hadamard value
        quantum_states = [
           qstate.QState((1.0, 0.0)),    # ket 0
           qstate.QState((0.0, 1.0)),    # ket 1
           qstate.QState((h, h)),        # ket plus
           qstate.QState((h, -h)),       # key minus
            
        ]
        targets = (0.0, 180.0, 90.0, 270.0)
        for psi, target in zip(quantum_states, targets):
            outcome = qstate.bloch_angle(psi)
            np.testing.assert_equal(outcome, target)

    def test_quantumstate_probability_distribution(self):
        h = 1.0 / np.sqrt(2) # hadamard value
        quantum_states = [
            qstate.QState((1.0, 0.0)),    # ket 0
            qstate.QState((0.0, 1.0)),    # ket 1
            qstate.QState((h, h)),        # ket plus
            qstate.QState((h, -h)),       # key minus
        ]
        target_vectors = [
            Vector((1.0, 0.0)),
            Vector((0.0, 1.0)),
            Vector((0.5, 0.5)),
            Vector((0.5, 0.5))
        ]
        for psi, target in zip(quantum_states, target_vectors):
            outcome = qstate.probability_distribution(psi)
            self.assertEqual(target,outcome)

    def test_quantumstate_reset(self):
        psi = qstate.KETPLUS
        result = qstate.reset(psi)
        target = qstate.KET0
        self.assertEqual(result,target)

# class TestQubit(unittest.TestCase):
  
#     def test_qubit_measure(self):
#         target = QuantumState(np.array([1,0]))
#         ket0 = Qubit(target)
#         outcome = ket0.measure()
#         np.testing.assert_array_almost_equal(outcome.state_vec, target.state_vec)

#         target = QuantumState(np.array([0,1]))
#         ket1 = Qubit(target)
#         outcome = ket1.measure()
#         np.testing.assert_array_almost_equal(outcome.state_vec, target.state_vec)

#     def test_qubit_eq(self):
#         x_state = QuantumState(np.array([1.0, 0.0]))
#         y_state = QuantumState(np.array([1.0, 0.0]))
#         x = Qubit(x_state)
#         y = Qubit(y_state)
#         assert_equal(x == y, True)

# if __name__ == "__main__":
#     unittest.main()
