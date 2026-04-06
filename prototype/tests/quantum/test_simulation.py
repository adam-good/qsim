import unittest
import math
import quantum.state as qstate
import quantum.simulation as qsim

class TestSimQubit(unittest.TestCase):
    def test_simqubit_reset(self):
        qubit = qsim.SimQubit(state=qstate.QState((0,1)))
        result = qubit.reset()
        self.assertEqual(result.state, qstate.KET0)
        self.assertEqual(result.ref_id, qubit.ref_id)

    def test_simqubit_measure(self):
        z_basis = qstate.Z_BASIS

        target_state = qstate.KET0
        qubit = qsim.SimQubit(state=target_state)
        result_qubit, result_state = qubit.measure(z_basis)
        self.assertEqual(result_qubit.state, target_state)  # Qubit's State Collapsed Correctly
        self.assertEqual(result_state, target_state)        # Correct Result State Returned
        self.assertEqual(qubit.ref_id, result_qubit.ref_id) # Qubit Reference Remained Static
        
        target_state = qstate.KET1
        qubit = qsim.SimQubit(state=target_state)
        result_qubit, result_state = qubit.measure(qstate.Z_BASIS)
        self.assertEqual(result_qubit.state, target_state)  # Qubit's State Collapsed Correctly
        self.assertEqual(result_state, target_state)        # Correct Result State Returned
        self.assertEqual(qubit.ref_id, result_qubit.ref_id) # Qubit Reference Remained Static

        N = 1000
        state_counts: dict[qstate.QState, int] = {qstate.KET0:0, qstate.KET1:0}
        for i in range(N):
            psi = qstate.QState( (1/math.sqrt(2), 1/math.sqrt(2)) )
            qubit, state = qsim.SimQubit(state=psi).measure(qstate.Z_BASIS)
            state_counts[state] += 1
        state_result = tuple(val / N for val in state_counts.values())
        target = (0.5, 0.5)
        for s, t in zip(state_result, target):
            self.assertAlmostEqual(s, t, places=1)

    def test_simqubit_ref_eq(self):
        psi = qstate.QState((1/math.sqrt(2), 1/math.sqrt(2)))
        omega = qstate.QState((0,1))

        q1 = qsim.SimQubit(ref_id=0, state=psi)
        q2 = qsim.SimQubit(ref_id=0, state=omega)
        self.assertTrue(q1.ref_eq(q2))

        q3 = qsim.SimQubit(ref_id=1, state=psi)
        self.assertFalse(q1.ref_eq(q3))

    def test_simqubit_state_eq(self):
        psi = qstate.QState((1/math.sqrt(2), 1/math.sqrt(2)))
        omega = qstate.QState((0,1))

        q1 = qsim.SimQubit(ref_id=0, state=psi)
        self.assertTrue(q1.state_eq(psi))
        self.assertFalse(q1.state_eq(omega))

    def test_simqubit_equiv(self):
        psi = qstate.QState((1/math.sqrt(2), 1/math.sqrt(2)))
        omega = qstate.QState((0,1))

        q1 = qsim.SimQubit(ref_id=0, state=psi)
        q2 = qsim.SimQubit(ref_id=1, state=psi)
        self.assertTrue(q1.equiv(q2))

        q3 = qsim.SimQubit(ref_id=0, state=omega)
        self.assertFalse(q1.equiv(q3))

class TestSimDevice(unittest.TestCase):
    def test_simdevice_n_qubits(self):
        n_qubits: int = 16
        n_alloc: int = 4
        qubits = [qsim.SimQubit(ref_id) for ref_id in range(n_qubits)]
        device = qsim.SimDevice(qubits)

        target: int = n_qubits
        result: int = device.n_available_qubits()
        self.assertEqual(target, result)

        target: int = n_qubits - n_alloc
        # Simulate Allocation to Test SimDevice.n_qubits()
        for i in range(n_alloc):
            device.alloc_tracker[i] = True
        result = device.n_available_qubits()
        self.assertEqual(result, target)
       

    def test_simdevice_n_alloc(self):
        qubits = [qsim.SimQubit(ref_id) for ref_id in range(16)]
        device = qsim.SimDevice(qubits)
        target = list(device.qubits.values())[:4]
        result = device._n_alloc(4)
        for (r,t) in zip(result, target):
            self.assertIs(r,t)

        target = len(qubits) - 4
        result = device.n_available_qubits()
        self.assertEqual(target, result)

    def test_simdevice_alloc(self):
        qubits = [qsim.SimQubit(ref_id) for ref_id in range(16)]
        device = qsim.SimDevice(qubits)
        target = list(device.qubits.values())[0]
        result = device._alloc()
        self.assertIs(target, result)
