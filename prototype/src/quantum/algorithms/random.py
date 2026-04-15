import quantum.gate as qgate
import quantum.device as qdev
import quantum.state as qstate


def _qstate_to_bit(state: qstate.QState) -> int:
    return 0 if state == qstate.KET0 else 1


def _qstates_to_bits(states: list[qstate.QState]) -> list[int]:
    return [_qstate_to_bit(state) for state in states]


def _prepare_qubits(
    qubits: list[qdev.Qubit], device: qdev.QuantumDevice
) -> list[qdev.Qubit]:
    return device.prepare_qubits(qubits, qgate.H_GATE)


def _measure_qubits(
    qubits: list[qdev.Qubit], device: qdev.QuantumDevice
) -> list[qstate.QState]:
    return device.measure_qubits(qubits, qstate.Z_BASIS)


def _batch_random_bits(n: int, device: qdev.QuantumDevice) -> list[int]:
    if not (n <= device.n_available_qubits()):
        raise ValueError(f"Qubit Alloc Overflow: {n} > {device.n_available_qubits()}")

    with device.alloc(n) as qubits:
        prepared_qubits: list[qdev.Qubit] = _prepare_qubits(qubits, device)
        measured_states: list[qstate.QState] = _measure_qubits(prepared_qubits, device)
        bits: list[int] = [_qstate_to_bit(state) for state in measured_states]
        return bits


def generate_random_bits(
    n: int,
    device: qdev.QuantumDevice,
) -> list[int]:
    result = []
    i = 0
    while i < n:
        batch_size = min(device.n_available_qubits(), n - i)
        result.extend(_batch_random_bits(batch_size, device))
        i += batch_size
    return result
