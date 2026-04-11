import quantum.device as qdev
import quantum.state as qstate


def qrng(
    n: int, device: qdev.QuantumDevice,
) -> list[int]:

    result = [0] * n
    i = 0
    while i < n:
        batch_size = min(device.n_available_qubits(), n - i)
        with device.n_alloc(batch_size) as qubits:
            for qubit in qubits:
                _, measurment = qubit.hadamard().measure(qstate.Z_BASIS)
                result[i] = 0 if measurment == qstate.KET0 else 1
                i += 1
    return result
