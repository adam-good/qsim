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
        for psi, target in zip(quantum_states, target_vectors):
            outcome = qstate.probability_distribution(qstate.Z_BASIS, psi)
            self.assertEqual(target,outcome)

    def test_quantumstate_reset(self):
        psi = qstate.KETPLUS
        result = qstate.reset(psi)
        target = qstate.KET0
        self.assertEqual(result,target)


    def test_quantumstate_collapse(self):
        psi = qstate.KET0
        target = qstate.KET0
        result = qstate.collapse(qstate.Z_BASIS, psi)
        self.assertEqual(result,target)

        psi = qstate.KET1
        target = qstate.KET1
        result = qstate.collapse(qstate.Z_BASIS, psi)
        self.assertEqual(result,target)


        # TODO: Should this really be done?
        N = 1000
        counts = {qstate.KET0:0, qstate.KET1:0}
        for i in range(N):
            psi = qstate.QState((1/math.sqrt(2), 1/math.sqrt(2)))
            counts[qstate.collapse(qstate.Z_BASIS, psi)] += 1
        result = tuple(val / N for val in counts.values())
        target = (0.5, 0.5)
        for a,b in zip(result, target):
            self.assertAlmostEqual(a,b,places=1)
            
