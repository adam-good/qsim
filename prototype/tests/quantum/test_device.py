import unittest
import quantum.state as qstate
import quantum.device as qdev
import quantum.gate as qgate


class TestQuantumDeviceInterface(unittest.TestCase):
    def test_alloc_context_manager(self):
        qubits = {i: qdev.Qubit(i) for i in range(4)}
        device = TestDevice(qubits, {})
        with device.alloc() as _:
            self.assertEqual(device.n_available_qubits(), 3)
        self.assertEqual(device.n_available_qubits(), 4)

    def test_n_alloc_context_manager(self):
        qubits = {i: qdev.Qubit(i) for i in range(4)}
        device = TestDevice(qubits, {})
        with device.n_alloc(2) as _:
            self.assertEqual(device.n_available_qubits(), 2)
        self.assertEqual(device.n_available_qubits(), 4)

    def test_apply_looks_up_gate_from_table(self):
        qubits = {0: qdev.Qubit(0, qstate.KET0)}
        gates = {qgate.Gates.H: qgate.COMMON_GATES[qgate.Gates.H]}
        device = TestDevice(qubits, gates)
        
        result = device.apply(0, qgate.Gates.H)
        
        self.assertEqual(result.state, qstate.KETPLUS)


class TestDevice(qdev.QuantumDevice):
    def __init__(self, qubits: dict[int, qdev.Qubit], gates: dict[qgate.Gates, qgate.QGate]):
        self._qubits = qubits
        self._gates = gates
        self._allocated: set[int] = set()

    def n_available_qubits(self) -> int:
        return len(self._qubits) - len(self._allocated)

    def _alloc(self) -> qdev.Qubit:
        for i in self._qubits:
            if i not in self._allocated:
                self._allocated.add(i)
                return self._qubits[i]
        raise RuntimeError("No qubits available")

    def _n_alloc(self, n: int) -> list[qdev.Qubit]:
        result = []
        for i in self._qubits:
            if i not in self._allocated and n > 0:
                self._allocated.add(i)
                result.append(self._qubits[i])
                n -= 1
        return result

    def _dealloc(self, qubit: qdev.Qubit):
        self._allocated.remove(qubit.id)

    def apply(self, qubit_id: int, gate: qgate.Gates) -> qdev.Qubit:
        current = self._qubits[qubit_id]
        matrix = self._gates[gate]
        new_state = matrix @ current.state
        return qdev.Qubit(qubit_id, new_state)


if __name__ == "__main__":
    unittest.main()