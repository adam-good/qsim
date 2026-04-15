import unittest
import quantum.state as qstate
import quantum.gate as qgate


class TestGates(unittest.TestCase):
    def test_i_gate(self):
        psi = qstate.KET0
        gate = qgate.I_GATE
        result = qgate.apply_gate(gate, psi)
        target = qstate.KET0
        self.assertEqual(result, target)
        
    def test_h_gate(self):
        psi = qstate.KET0
        gate = qgate.H_GATE
        result = qgate.apply_gate(gate, psi)
        target = qstate.KETPLUS
        self.assertEqual(result, target)

    def test_x_gate(self):
        psi = qstate.KET0
        gate = qgate.X_GATE
        result = qgate.apply_gate(gate, psi)
        target = qstate.KET1
        self.assertEqual(result, target)

    def test_gates_enum_values(self):
        self.assertEqual(qgate.Gates.H.value, 0)
        self.assertEqual(qgate.Gates.X.value, 1)

    def test_common_gates_lookup(self):
        self.assertTrue(isinstance(qgate.COMMON_GATES[qgate.Gates.H], qgate.QGate))
        self.assertTrue(isinstance(qgate.COMMON_GATES[qgate.Gates.X], qgate.QGate))

    def test_apply_gate(self):
        psi = qstate.KET0
        gate = qgate.COMMON_GATES[qgate.Gates.H]
        result = qgate.apply_gate(gate, psi)
        self.assertEqual(result, qstate.KETPLUS)


if __name__ == "__main__":
    unittest.main()
