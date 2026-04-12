import unittest
import quantum.state as qstate
import quantum.gate as qgate
import quantum.simulation as qsim


class TestSimQubitData(unittest.TestCase):
    def test_qubit_has_id_and_state(self):
        qubit = qsim.SimQubit(id=0, state=qstate.KET0)
        self.assertEqual(qubit.id, 0)
        self.assertEqual(qubit.state, qstate.KET0)

    def test_qubit_default_state(self):
        qubit = qsim.SimQubit(id=5)
        self.assertEqual(qubit.state, qstate.KET0)

    def test_qubit_frozen_immutable(self):
        qubit = qsim.SimQubit(id=0, state=qstate.KET1)
        with self.assertRaises(AttributeError):
            qubit.id = 1


class TestSimDeviceApply(unittest.TestCase):
    def test_apply_h_gate(self):
        qubits = {0: qsim.SimQubit(0, qstate.KET0)}
        device = qsim.SimDevice(qubits=qubits)
        
        result = device.apply(0, qgate.Gates.H)
        
        self.assertEqual(result.state, qstate.KETPLUS)

    def test_apply_x_gate(self):
        qubits = {0: qsim.SimQubit(0, qstate.KET0)}
        device = qsim.SimDevice(qubits=qubits)
        
        result = device.apply(0, qgate.Gates.X)
        
        self.assertEqual(result.state, qstate.KET1)

    def test_apply_sequential_gates(self):
        qubits = {0: qsim.SimQubit(0, qstate.KET0)}
        device = qsim.SimDevice(qubits=qubits)
        
        result = device.apply(0, qgate.Gates.X)
        result = device.apply(0, qgate.Gates.H)
        
        self.assertEqual(result.state, qstate.KETMINUS)


class TestSimDeviceAllocate(unittest.TestCase):
    def test_simdevice_n_qubits(self):
        n_qubits = 16
        n_alloc = 4
        qubits = {i: qsim.SimQubit(i) for i in range(n_qubits)}
        device = qsim.SimDevice(qubits=qubits)

        target = n_qubits
        result = device.n_available_qubits()
        self.assertEqual(target, result)

        target = n_qubits - n_alloc
        for i in range(n_alloc):
            device.allocated.add(i)
        result = device.n_available_qubits()
        self.assertEqual(target, result)

    def test_simdevice_n_alloc(self):
        qubits = {i: qsim.SimQubit(i) for i in range(16)}
        device = qsim.SimDevice(qubits=qubits)
        
        result = device._n_alloc(4)
        
        self.assertEqual(len(result), 4)
        self.assertEqual(len(device.allocated), 4)

    def test_simdevice_alloc(self):
        qubits = {i: qsim.SimQubit(i) for i in range(16)}
        device = qsim.SimDevice(qubits=qubits)
        
        result = device._alloc()
        
        self.assertEqual(result.id, 0)
        self.assertIn(0, device.allocated)

    def test_simdevice_dealloc(self):
        qubits = {i: qsim.SimQubit(i) for i in range(4)}
        device = qsim.SimDevice(qubits=qubits)
        
        qubit = device._alloc()
        device._dealloc(qubit)
        
        self.assertEqual(device.n_available_qubits(), 4)


class TestSimDeviceMeasure(unittest.TestCase):
    def test_measure_via_device_apply(self):
        qubits = {0: qsim.SimQubit(0, qstate.KET0)}
        device = qsim.SimDevice(qubits=qubits)
        
        device.apply(0, qgate.Gates.H)
        current = device.qubits[0]
        collapsed = qstate.collapse(qstate.Z_BASIS, current.state)
        
        self.assertIn(collapsed, [qstate.KET0, qstate.KET1])

    def test_measure_distribution(self):
        qubits = {0: qsim.SimQubit(0, qstate.KET0)}
        device = qsim.SimDevice(qubits=qubits)
        
        device.apply(0, qgate.Gates.H)
        current = device.qubits[0]
        
        N = 1000
        counts = {qstate.KET0: 0, qstate.KET1: 0}
        for _ in range(N):
            collapsed = qstate.collapse(qstate.Z_BASIS, current.state)
            counts[collapsed] += 1
        
        for state, count in counts.items():
            self.assertAlmostEqual(count / N, 0.5, delta=0.05)


if __name__ == "__main__":
    unittest.main()