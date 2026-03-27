import unittest
import math
import quantum.state as qstate
from utils.math.vector import Vector

class TestQuantumState(unittest.TestCase):
    def test_quantumestate_angles(self):
        h = 1.0 / math.sqrt(2) # hadamard value
        qubits = [
           qstate.QState((1.0, 0.0)),    # ket 0
           qstate.QState((0.0, 1.0)),    # ket 1
           qstate.QState((h, h)),        # ket plus
           qstate.QState((h, -h)),       # key minus
            
        ]
        targets = [0.0, 90.0, 45.0, 315.0]
        for psi, target in zip(qubits, targets):
            outcome = qstate.angle(psi)
            self.assertEqual(outcome, target)

    def test_quantumstate_bloch_angles(self):
        h = 1.0 / math.sqrt(2) # hadamard value
        quantum_states = [
           qstate.QState((1.0, 0.0)),    # ket 0
           qstate.QState((0.0, 1.0)),    # ket 1
           qstate.QState((h, h)),        # ket plus
           qstate.QState((h, -h)),       # key minus
            
        ]
        targets = (0.0, 180.0, 90.0, 270.0)
        for psi, target in zip(quantum_states, targets):
            outcome = qstate.bloch_angle(psi)
            self.assertEqual(outcome, target)

    def test_quantumstate_probability_distribution(self):
        h = 1.0 / math.sqrt(2) # hadamard value
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
        z_basis = qstate.Z_BASIS
        for psi, target in zip(quantum_states, target_vectors):
            outcome = qstate.probability_distribution(z_basis, psi)
            self.assertEqual(target,outcome)

    def test_quantumstate_reset(self):
        psi = qstate.KETPLUS
        result = qstate.reset(psi)
        target = qstate.KET0
        self.assertEqual(result,target)

    # TODO: Collapse to other basis
    def test_quantumstate_collapse(self):
        tests = [
            (qstate.Z_BASIS, qstate.KET0, qstate.KET0),
            (qstate.Z_BASIS, qstate.KET1, qstate.KET1),
            (qstate.X_BASIS, qstate.KETPLUS, qstate.KETPLUS),
            (qstate.X_BASIS, qstate.KETMINUS, qstate.KETMINUS)
        ]

        for (basis, psi, target) in tests:
            result = qstate.collapse(basis, psi)
            self.assertEqual(result, target)



           
