import unittest
import quantum.state as qstate
import quantum.device as qdev


class TestQubitImpl(qdev.Qubit):
    def __init__(self, id: int):
        self._id = id

    @property
    def ref_id(self) -> int:
        return self._id

    def copy(self) -> qdev.Qubit:
        return TestQubitImpl(self._id)

    def measure(
        self, basis: tuple[qstate.QState, qstate.QState]
    ) -> tuple[qdev.Qubit, qstate.QState]:
        return (self, qstate.KET0)

    def reset(self) -> qdev.Qubit:
        return self

    def hadamard(self) -> qdev.Qubit:
        return self

    def negate(self) -> qdev.Qubit:
        return self


class TestDeviceImpl(qdev.QuantumDevice):
    def __init__(self, n_qubits: int):
        self._qubits = [TestQubitImpl(i) for i in range(n_qubits)]
        self._allocated: set[int] = set()
        self._dealloc_calls: list[int] = []

    def copy(self, qubit: qdev.Qubit) -> qdev.Qubit:
        return qubit.copy()

    def n_available_qubits(self) -> int:
        total = len(self._qubits)
        allocd = len(self._allocated)
        return total - allocd

    def _alloc(self) -> qdev.Qubit:
        for i in range(len(self._qubits)):
            if i not in self._allocated:
                self._allocated.add(i)
                return self._qubits[i]
        raise RuntimeError("No qubits available")

    def _n_alloc(self, n: int) -> list[qdev.Qubit]:
        result = []
        for i in range(len(self._qubits)):
            if i not in self._allocated and n > 0:
                self._allocated.add(i)
                result.append(self._qubits[i])
                n -= 1
        return result

    def _dealloc(self, qubit: qdev.Qubit):
        self._allocated.remove(qubit.ref_id)
        self._dealloc_calls.append(qubit.ref_id)


class TestQuantumDeviceInterface(unittest.TestCase):
    def test_alloc_context_manager(self):
        device = TestDeviceImpl(4)
        with device.alloc() as _:
            self.assertEqual(device.n_available_qubits(), 3)
        self.assertEqual(device.n_available_qubits(), 4)

    def test_n_alloc_context_manager(self):
        device = TestDeviceImpl(4)
        with device.n_alloc(2) as _:
            self.assertEqual(device.n_available_qubits(), 2)
        self.assertEqual(device.n_available_qubits(), 4)

    def test_alloc_resets_qubit_on_exit(self):
        device = TestDeviceImpl(4)
        with device.alloc() as _:
            pass
        self.assertIn(0, device._dealloc_calls)

    def test_n_alloc_resets_all_qubits_on_exit(self):
        device = TestDeviceImpl(4)
        with device.n_alloc(2) as _:
            pass
        self.assertEqual(len(device._dealloc_calls), 2)


class TestQubitInterface(unittest.TestCase):
    def test_qubit_is_abstract(self):
        with self.assertRaises(TypeError):
            qdev.Qubit()


if __name__ == "__main__":
    unittest.main()
