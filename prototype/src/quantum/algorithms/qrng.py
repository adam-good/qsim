import quantum.device as qdev
import quantum.state as qstate

def qrng(n: int, device: qdev.QuantumDevice, map: dict[qstate.QState, int]) -> list[int]:
    result = n*[2]
    i = 0
    while i < n:
        n_qubits = min(device.n_available_qubits(), n - i)
        with device.n_alloc(n_qubits) as qubits:
            for qubit in qubits:
                qubit = qubit.hadamard()
                qubit, measurment = qubit.measure(qstate.Z_BASIS)
                result[i] = map[measurment]
                i += 1
    return result
