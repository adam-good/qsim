import unittest
import math
import quantum.state as qstate
import quantum.gate as qgate

class TestGates(unittest.TestCase):
    def test_h_gate(self):
        qubit = qstate.KET0
        result = qgate.hgate(qubit)
        target = qstate.QState((1, 1)) / math.sqrt(2)
        self.assertEqual(result, target)

    def test_x_gate(self):
        qubit = qstate.KET0
        result = qgate.xgate(qubit)
        target = qstate.QState((0,1))
        self.assertEqual(result, target)


if __name__ == "__main__":
    unittest.main()
