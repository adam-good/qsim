import unittest
import math
import random
import utils.math.vector as vector
import quantum.state as qstate

HADAMARD_CONST = qstate.HADAMARD_CONST


class TestQuantumState(unittest.TestCase):
    def test_quantumestate_angles(self):
        h = 1.0 / math.sqrt(2)  # hadamard value
        qubits = [
            qstate.QState(vector.Vector((1.0, 0.0))),  # ket 0
            qstate.QState(vector.Vector((0.0, 1.0))),  # ket 1
            qstate.QState(vector.Vector((h, h))),  # ket plus
            qstate.QState(vector.Vector((h, -h))),  # key minus
        ]
        targets = [0.0, 90.0, 45.0, 315.0]
        for psi, target in zip(qubits, targets):
            outcome = qstate.angle(psi)
            self.assertEqual(outcome, target)

    def test_quantumstate_bloch_angles(self):
        h = 1.0 / math.sqrt(2)  # hadamard value
        quantum_states = [
            qstate.QState(vector.Vector((1.0, 0.0))),  # ket 0
            qstate.QState(vector.Vector((0.0, 1.0))),  # ket 1
            qstate.QState(vector.Vector((h, h))),  # ket plus
            qstate.QState(vector.Vector((h, -h))),  # key minus
        ]
        targets = (0.0, 180.0, 90.0, 270.0)
        for psi, target in zip(quantum_states, targets):
            outcome = qstate.bloch_angle(psi)
            self.assertEqual(outcome, target)

    def test_quantumstate_probability_distribution(self):
        h = 1.0 / math.sqrt(2)  # hadamard value
        quantum_states = [
            qstate.QState(vector.Vector((1.0, 0.0))),  # ket 0
            qstate.QState(vector.Vector((0.0, 1.0))),  # ket 1
            qstate.QState(vector.Vector((h, h))),  # ket plus
            qstate.QState(vector.Vector((h, -h))),  # key minus
        ]
        target_vectors = [
            vector.Vector((1.0, 0.0)),
            vector.Vector((0.0, 1.0)),
            vector.Vector((0.5, 0.5)),
            vector.Vector((0.5, 0.5)),
        ]
        z_basis = qstate.Z_BASIS
        for psi, target in zip(quantum_states, target_vectors):
            outcome = qstate.probability_distribution(z_basis, psi)
            self.assertEqual(target, outcome)

    def test_quantumstate_reset(self):
        psi = qstate.KETPLUS
        result = qstate.reset(psi)
        target = qstate.KET0
        self.assertEqual(result, target)

    def test_quantumstate_collapse(self):
        tests = [
            (qstate.Z_BASIS, qstate.KET0, qstate.KET0),
            (qstate.Z_BASIS, qstate.KET1, qstate.KET1),
            (qstate.X_BASIS, qstate.KETPLUS, qstate.KETPLUS),
            (qstate.X_BASIS, qstate.KETMINUS, qstate.KETMINUS),
        ]

        for basis, psi, target in tests:
            result = qstate.collapse(basis, psi)
            self.assertEqual(result, target)

    def test_quantumstate_collapse_reproducible(self):
        rng1 = random.Random(42)
        rng2 = random.Random(42)
        superposition = qstate.QState(
            vector.Vector((1 / math.sqrt(2), 1 / math.sqrt(2)))
        )
        results1 = [
            qstate.collapse(qstate.Z_BASIS, superposition, rng1) for _ in range(10)
        ]
        results2 = [
            qstate.collapse(qstate.Z_BASIS, superposition, rng2) for _ in range(10)
        ]
        self.assertEqual(results1, results2)

    def test_quantum_superposition_collapse(self):
        basises = (qstate.Z_BASIS, qstate.X_BASIS)
        for basis in basises:
            w, v = basis
            superposition = qstate.QState((w.vector + v.vector) * HADAMARD_CONST)
            N = 1000
            shots = [qstate.collapse(basis, superposition) for _ in range(N)]
            result_w = len([x for x in shots if x == w]) / N
            result_v = len([x for x in shots if x == v]) / N
            self.assertAlmostEqual(result_w, 0.5, delta=0.05)
            self.assertAlmostEqual(result_v, 0.5, delta=0.05)
