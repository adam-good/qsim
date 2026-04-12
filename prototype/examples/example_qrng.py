from quantum.algorithms.random import generate_random_bits
import quantum.simulation as qsim

def main():
    n_qubits = 4
    qubits = {i: qsim.SimQubit(i) for i in range(n_qubits)}
    device = qsim.SimDevice(qubits=qubits)
    
    result = generate_random_bits(16, device)
    print(result)


if __name__ == "__main__":
    main()