import utils.math.bit as bit
import quantum.gate as qgate
import quantum.device as qdev
import quantum.state as qstate


def _qstate_to_bit(state: qstate.QState) -> bit.Bit:
    return bit.BIT_0 if state == qstate.KET0 else bit.BIT_1


def _qstates_to_bits(states: list[qstate.QState]) -> list[bit.Bit]:
    return [_qstate_to_bit(state) for state in states]


def _prepare_qubits(
    qubits: list[qdev.Qubit], device: qdev.QuantumDevice
) -> list[qdev.Qubit]:
    return device.prepare_qubits(qubits, qgate.H_GATE)


def _measure_qubits(
    qubits: list[qdev.Qubit], device: qdev.QuantumDevice
) -> list[qstate.QState]:
    return device.measure_qubits(qubits, qstate.Z_BASIS)


def _batch_random_bits(n: int, device: qdev.QuantumDevice) -> list[bit.Bit]:
    if not (n <= device.n_available_qubits()):
        raise ValueError(f"Qubit Alloc Overflow: {n} > {device.n_available_qubits()}")

    with device.alloc(n) as qubits:
        prepared_qubits: list[qdev.Qubit] = _prepare_qubits(qubits, device)
        measured_states: list[qstate.QState] = _measure_qubits(prepared_qubits, device)
        bits: list[bit.Bit] = [_qstate_to_bit(state) for state in measured_states]
        return bits


def generate_random_bits(
    n: int,
    device: qdev.QuantumDevice,
) -> list[bit.Bit]:
    result: list[bit.Bit] = []
    i = 0
    while i < n:
        batch_size = min(device.n_available_qubits(), n - i)
        result.extend(_batch_random_bits(batch_size, device))
        i += batch_size
    return result


def random_bit(device: qdev.QuantumDevice) -> int:
    with device.alloc() as qubit:
        _, state = qubit.hadamard().measure(qstate.Z_BASIS)
        return _qubit_to_bit(state)
