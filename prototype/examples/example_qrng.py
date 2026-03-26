from quantum.simulation import SimDevice
from quantum.algorithms.qrng import qrng
import quantum.state as qstate

def main():
    bitmap = {
        qstate.KET0:0,
        qstate.KET1:1,
    }
    device = SimDevice(4)
    result = [qrng(device, bitmap) for _ in range(16)]
    print(result)

if __name__ == "__main__":
    main()
