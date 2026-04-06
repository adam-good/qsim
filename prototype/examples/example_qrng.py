from quantum.algorithms.qrng import qrng
import quantum.simulation as qsim
import quantum.state as qstate

def main():
    bitmap = {
        qstate.KET0:0,
        qstate.KET1:1,
    }
    n_qubits = 4
    device = qsim.SimDevice([qsim.SimQubit(ref_id) for ref_id in range(n_qubits)])
    result = [qrng(device, bitmap) for _ in range(16)]
    print(result)

if __name__ == "__main__":
    main()
