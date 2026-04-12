import unittest
import quantum.gate as qgate
import quantum.state as qstate
import quantum.device as qdev
import quantum.algorithms.random as random


class MockQubit(qdev.Qubit):
    def __init__(self, id: int, state: qstate.QState):
        self._id = id
        self._state = state

    @property
    def ref_id(self) -> int:
        return self._id

    def copy(self) -> qdev.Qubit:
        return MockQubit(self._id, self._state)

    def measure(
        self, basis: tuple[qstate.QState, qstate.QState]
    ) -> tuple[qdev.Qubit, qstate.QState]:
        collapsed = qstate.collapse(basis, self._state)
        return (MockQubit(self._id, collapsed), collapsed)

    def reset(self) -> qdev.Qubit:
        return MockQubit(self._id, qstate.KET0)

    def hadamard(self) -> qdev.Qubit:
        new_state = qgate.hadamard(self._state)
        return MockQubit(self._id, new_state)

    def negate(self) -> qdev.Qubit:
        new_state = qgate.negate(self._state)
        return MockQubit(self._id, new_state)


class MockDevice(qdev.QuantumDevice):
    def __init__(self, n_qubits: int):
        self._qubits = [MockQubit(i, qstate.KET0) for i in range(n_qubits)]
        self._allocated: set[int] = set()

    def copy(self, qubit: qdev.Qubit) -> qdev.Qubit:
        return qubit.copy()

    def n_available_qubits(self) -> int:
        return len(self._qubits) - len(self._allocated)

    def _alloc(self) -> qdev.Qubit:
        available = set(range(len(self._qubits))) - self._allocated
        qubit_id = min(available)
        self._allocated.add(qubit_id)
        return self._qubits[qubit_id]

    def _n_alloc(self, n: int) -> list[qdev.Qubit]:
        available = sorted(set(range(len(self._qubits))) - self._allocated)
        selected = available[:n]
        for i in selected:
            self._allocated.add(i)
        return [self._qubits[i] for i in selected]

    def _dealloc(self, qubit: qdev.Qubit):
        self._allocated.remove(qubit.ref_id)

    def pop_qubit(self, qubit: qdev.Qubit) -> qdev.Qubit:
        assert qubit.ref_id in self._allocated
        self._allocated.remove(qubit.ref_id)
        return self._qubits[qubit.ref_id]

    def push_qubit(self, qubit: qdev.Qubit):
        assert qubit.ref_id not in self._allocated
        self._qubits.append(qubit)
        self._allocated.add(qubit.ref_id)

    def transfer(self, device: qdev.QuantumDevice, qubit: qdev.Qubit):
        qubit = self.pop_qubit(qubit)
        device.push_qubit(qubit)


class TestQRNG(unittest.TestCase):
    def test_qubit_to_bit_ket0(self):
        result = random._qubit_to_bit(qstate.KET0)
        self.assertEqual(result, 0)

    def test_qubit_to_bit_ket1(self):
        result = random._qubit_to_bit(qstate.KET1)
        self.assertEqual(result, 1)

    def test_batch_random_bits(self):
        device = MockDevice(4)
        result = random._batch_random_bits(4, device)
        self.assertEqual(len(result), 4)
        for bit in result:
            self.assertIn(bit, [0, 1])

    def test_batch_random_bits_allocation(self):
        device = MockDevice(4)
        random._batch_random_bits(4, device)
        self.assertEqual(device.n_available_qubits(), 4)

    def test_generate_random_bits_single_batch(self):
        device = MockDevice(8)
        result = random.generate_random_bits(4, device)
        self.assertEqual(len(result), 4)

    def test_generate_random_bits_multiple_batches(self):
        device = MockDevice(4)
        result = random.generate_random_bits(6, device)
        self.assertEqual(len(result), 6)

    def test_generate_random_bits_exhausts_device(self):
        device = MockDevice(2)
        result = random.generate_random_bits(8, device)
        self.assertEqual(len(result), 8)


if __name__ == "__main__":
    unittest.main()
