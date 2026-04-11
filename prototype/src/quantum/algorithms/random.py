import quantum.device as qdev
import quantum.state as qstate


def _qubit_to_bit(state: qstate.QState) -> int:
    return 0 if state == qstate.KET0 else 1


def _batch_random_bits(n: int, device: qdev.QuantumDevice) -> list[int]:
    assert n <= device.n_available_qubits()

    with device.n_alloc(n) as qubits:
        measurements = [qubit.hadamard().measure(qstate.Z_BASIS) for qubit in qubits]
        bits = [_qubit_to_bit(state) for _,state in measurements]
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

def random_bit(device: qdev.QuantumDevice) -> int:
    with device.alloc() as qubit:
        _, state = qubit.hadamard().measure(qstate.Z_BASIS)
        return _qubit_to_bit(state)
