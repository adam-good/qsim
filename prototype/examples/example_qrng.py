import quantum.algorithms.random as qrand
import quantum.device as qdev


def main():
    n_qubits = 4
    qubits = [qdev.Qubit(ref_id) for ref_id in range(n_qubits)]
    device = qdev.QuantumDevice(qubits)
    result = qrand.generate_random_bits(16, device)
    print(result)


if __name__ == "__main__":
    main()
