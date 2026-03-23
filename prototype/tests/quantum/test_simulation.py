import unittest
import quantum.state as qstate
import quantum.simulation as qsim

class TestSimQubit(unittest.TestCase):
    def test_simqubit_reset(self):
        qubit = qsim.SimQubit(qstate.QState((0,1)))
        result = qubit.reset()
        target = qstate.KET0
        self.assertEqual(result, target)
