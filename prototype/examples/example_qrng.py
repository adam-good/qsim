from quantum.algorithms.qrng import qrng
import quantum.simulation as qsim


def main():
    n_qubits = 4
    qubits = [qsim.SimQubit(ref_id) for ref_id in range(n_qubits)]
    device = qsim.SimDevice(qubits)
    result = qrng(16, device)
    print(result)


if __name__ == "__main__":
    main()
