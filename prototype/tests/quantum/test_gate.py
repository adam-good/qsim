import unittest
import quantum.state as qstate
import quantum.gate as qgate


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


if __name__ == "__main__":
    unittest.main()
