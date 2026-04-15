import unittest
import quantum.gate as qgate
import quantum.state as qstate
import quantum.device as qdev
import quantum.algorithms.random as random


class MockQubit(qdev.Qubit):
    @property
    def ref_id(self) -> int:
        return self._id

    @property
    def state(self) -> qstate.QState:
        return self._state

    def __repr__(self) -> str:
        return f"MockQubit({self._id}, {self._state})"


class MockDevice(qdev.QuantumDevice):
    def __init__(self, n_qubits: int):
        qubits = [MockQubit(i, qstate.KET0) for i in range(n_qubits)]
        super().__init__(qubits)

    def prepare_single_qubit(self, qubit: qdev.Qubit, gate: qgate.QGate) -> qdev.Qubit:
        new_state = qgate.apply_gate(gate, qubit._state)
        return MockQubit(qubit.ref_id, new_state)

    def measure_single_qubit(
        self, qubit: qdev.Qubit, basis: qstate.QBasis
    ) -> qstate.QState:
        collapsed = qstate.collapse(basis, qubit._state)
        return collapsed


class TestQRNG(unittest.TestCase):
    def test_qstate_to_bit_ket0(self):
        result = random._qstate_to_bit(qstate.KET0)
        self.assertEqual(result, 0)

    def test_qstate_to_bit_ket1(self):
        result = random._qstate_to_bit(qstate.KET1)
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
