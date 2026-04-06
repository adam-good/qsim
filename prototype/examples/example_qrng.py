from quantum.algorithms.qrng import qrng
import quantum.simulation as qsim
import quantum.state as qstate

def main():
    n_qubits = 4
    device = qsim.SimDevice([qsim.SimQubit(ref_id) for ref_id in range(n_qubits)])
    result = qrng(16, device)
    print(result)

if __name__ == "__main__":
    main()
