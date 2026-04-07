import quantum.device as qdev
import quantum.state as qstate


def qrng(
    n: int, device: qdev.QuantumDevice, state_map: dict[qstate.QState, int] | None
) -> list[int]:
    if state_map is None:
        state_map = {qstate.KET0: 0, qstate.KET1: 1}

    result = n * [2]
    i = 0
    while i < n:
        batch_size = min(device.n_available_qubits(), n - i)
        with device.n_alloc(batch_size) as qubits:
            for qubit in qubits:
                _, measurment = qubit.hadamard().measure(qstate.Z_BASIS)
                result[i] = state_map[measurment]
                i += 1
    return result
