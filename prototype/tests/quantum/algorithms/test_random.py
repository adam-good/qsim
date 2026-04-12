import unittest
import quantum.gate as qgate
import quantum.state as qstate
import quantum.device as qdev


class MockDevice(qdev.QuantumDevice):
    def __init__(self, n_qubits: int):
        self._qubits = {i: qdev.Qubit(i, qstate.KET0) for i in range(n_qubits)}
        self._gates = qgate.COMMON_GATES
        self._allocated: set[int] = set()

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
        self._allocated.remove(qubit.id)

    def apply(self, qubit_id: int, gate: qgate.Gates) -> qdev.Qubit:
        current = self._qubits[qubit_id]
        matrix = self._gates[gate]
        new_state = matrix @ current.state
        new_qubit = qdev.Qubit(qubit_id, new_state)
        self._qubits[qubit_id] = new_qubit
        return new_qubit


class TestQRNG(unittest.TestCase):
    def test_qubit_to_bit_ket0(self):
        from quantum.algorithms.random import _qubit_to_bit
        result = _qubit_to_bit(qstate.KET0)
        self.assertEqual(result, 0)

    def test_qubit_to_bit_ket1(self):
        from quantum.algorithms.random import _qubit_to_bit
        result = _qubit_to_bit(qstate.KET1)
        self.assertEqual(result, 1)

    def test_batch_random_bits(self):
        from quantum.algorithms.random import _batch_random_bits
        device = MockDevice(4)
        result = _batch_random_bits(4, device)
        self.assertEqual(len(result), 4)
        for bit in result:
            self.assertIn(bit, [0, 1])

    def test_batch_random_bits_allocation(self):
        from quantum.algorithms.random import _batch_random_bits
        device = MockDevice(4)
        _batch_random_bits(4, device)
        self.assertEqual(device.n_available_qubits(), 4)

    def test_generate_random_bits_single_batch(self):
        from quantum.algorithms.random import generate_random_bits
        device = MockDevice(8)
        result = generate_random_bits(4, device)
        self.assertEqual(len(result), 4)

    def test_generate_random_bits_multiple_batches(self):
        from quantum.algorithms.random import generate_random_bits
        device = MockDevice(4)
        result = generate_random_bits(6, device)
        self.assertEqual(len(result), 6)

    def test_generate_random_bits_exhausts_device(self):
        from quantum.algorithms.random import generate_random_bits
        device = MockDevice(2)
        result = generate_random_bits(8, device)
        self.assertEqual(len(result), 8)


if __name__ == "__main__":
    unittest.main()