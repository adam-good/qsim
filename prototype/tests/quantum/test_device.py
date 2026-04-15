import unittest
import quantum.device as qdev


class TestQubitImpl(qdev.Qubit):
    def __init__(self, id: int):
        self._id = id

    @property
    def ref_id(self) -> int:
        return self._id


class TestDeviceImpl(qdev.QuantumDevice):
    def __init__(self, n_qubits: int):
        qubits = [TestQubitImpl(i) for i in range(n_qubits)]
        super().__init__(qubits)
        self._dealloc_calls: list[int] = []

    def _dealloc(self, qubit: qdev.Qubit):
        super()._dealloc(qubit)
        self._dealloc_calls.append(qubit.ref_id)


class TestQuantumDeviceInterface(unittest.TestCase):
    def test_alloc_single_context_manager(self):
        device = TestDeviceImpl(4)
        with device.alloc_single() as _:
            self.assertEqual(device.n_available_qubits(), 3)
        self.assertEqual(device.n_available_qubits(), 4)

    def test_alloc_context_manager(self):
        device = TestDeviceImpl(4)
        with device.alloc(2) as _:
            self.assertEqual(device.n_available_qubits(), 2)
        self.assertEqual(device.n_available_qubits(), 4)

    def test_alloc_single_resets_qubit_on_exit(self):
        device = TestDeviceImpl(4)
        with device.alloc_single() as _:
            pass
        self.assertIn(0, device._dealloc_calls)

    def test_alloc_resets_all_qubits_on_exit(self):
        device = TestDeviceImpl(4)
        with device.alloc(2) as _:
            pass
        self.assertEqual(len(device._dealloc_calls), 2)


if __name__ == "__main__":
    unittest.main()
