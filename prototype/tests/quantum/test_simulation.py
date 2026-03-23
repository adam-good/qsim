import unittest
import math
import quantum.state as qstate
import quantum.simulation as qsim

class TestSimQubit(unittest.TestCase):
    def test_simqubit_reset(self):
        qubit = qsim.SimQubit(qstate.QState((0,1)))
        result = qubit.reset()
        target = qstate.KET0
        self.assertEqual(result, target)

    def test_simqubit_measure(self):
        target_state = qstate.KET0
        target_qubit = qsim.SimQubit(target_state)
        qubit = qsim.SimQubit(target_state)
        result_qubit, result_state = qubit.measure()
        self.assertEqual(result_qubit, target_qubit)
        self.assertEqual(result_state, target_state)

        
        target_state = qstate.KET1
        target_qubit = qsim.SimQubit(target_state)
        qubit = qsim.SimQubit(target_state)
        result_qubit, result_state = qubit.measure()
        self.assertEqual(result_qubit, target_qubit)
        self.assertEqual(result_state, target_state)

        N = 1000
        ket0 = qsim.SimQubit(qstate.KET0)
        ket1 = qsim.SimQubit(qstate.KET1)
        state_counts = {qstate.KET0:0, qstate.KET1:0}
        qubit_counts = {ket0:0, ket1:0}
        for i in range(N):
            psi = qstate.QState( (1/math.sqrt(2), 1/math.sqrt(2)) )
            qubit, state = qsim.SimQubit(psi).measure()
            qubit_counts[qubit] += 1
            state_counts[state] += 1
        state_result = tuple(val / N for val in state_counts.values())
        qubit_result = tuple(val / N for val in qubit_counts.values())
        target = (0.5, 0.5)
        for (q,s,t) in zip(qubit_result, state_result, target):
            self.assertAlmostEqual(q,t,places=1)
            self.assertAlmostEqual(s,t, places=1)
