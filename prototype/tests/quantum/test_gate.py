import unittest
import quantum.state as qstate
import quantum.gate as qgate
from utils.math.matrix import Matrix


class TestGates(unittest.TestCase):
    def test_h_gate(self):
        psi = qstate.KET0
        result = qgate.hgate(psi)
        target = qstate.KETPLUS
        self.assertEqual(result, target)

    def test_x_gate(self):
        psi = qstate.KET0
        result = qgate.xgate(psi)
        target = qstate.KET1
        self.assertEqual(result, target)

    def test_apply_gate_check_unitary_true(self):
        psi = qstate.KET0
        gate = qgate.COMMON_GATES[qgate.Gates.H]
        result = qgate.apply_gate(psi, gate, check_unitary=True)
        self.assertEqual(result, qstate.KETPLUS)

    def test_apply_gate_non_unitary_raises(self):
        non_unitary = Matrix(((1, 0), (0, 2)))
        psi = qstate.KET0
        with self.assertRaises(Exception) as ctx:
            qgate.apply_gate(psi, non_unitary, check_unitary=True)
        self.assertIn("Not Unitary", str(ctx.exception))

    def test_gates_enum_values(self):
        self.assertEqual(qgate.Gates.H.value, 0)
        self.assertEqual(qgate.Gates.X.value, 1)

    def test_common_gates_lookup(self):
        self.assertTrue(isinstance(qgate.COMMON_GATES[qgate.Gates.H], Matrix))
        self.assertTrue(isinstance(qgate.COMMON_GATES[qgate.Gates.X], Matrix))

    def test_hadamard_alias(self):
        self.assertEqual(qgate.hadamard, qgate.hgate)

    def test_negate_alias(self):
        self.assertEqual(qgate.negate, qgate.xgate)

    def test_h_alias(self):
        self.assertEqual(qgate.h, qgate.hgate)

    def test_x_alias(self):
        self.assertEqual(qgate.x, qgate.xgate)


if __name__ == "__main__":
    unittest.main()
