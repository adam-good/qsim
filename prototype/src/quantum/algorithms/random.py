import quantum.device as qdev
import quantum.state as qstate
import quantum.gate as qgate


def _qubit_to_bit(state: qstate.QState) -> int:
    return 0 if state == qstate.KET0 else 1


def _batch_random_bits(n: int, device: qdev.QuantumDevice) -> list[int]:
    assert n <= device.n_available_qubits()

    with device.n_alloc(n) as qubits:
        bits = []
        for qubit in qubits:
            after_h = device.apply(qubit.id, qgate.Gates.H)
            collapsed = qstate.collapse(qstate.Z_BASIS, after_h.state)
            bits.append(_qubit_to_bit(collapsed))
        return bits


def generate_random_bits(
    n: int, device: qdev.QuantumDevice,
) -> list[int]:

    result = []
    i = 0
    while i < n:
        batch_size = min(device.n_available_qubits(), n - i)
        result.extend(_batch_random_bits(batch_size, device))
        i += batch_size
    return result