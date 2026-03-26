from quantum.device import QuantumDevice as QDevice
from quantum.simulation import SimDevice
import quantum.state as qstate

def qrng(device: QDevice, bitmap: dict[qstate.QState, int]) -> int:
    with device.alloc() as psi:
        psi.hadamard()
        psi, measurement = psi.measure()
    return bitmap[measurement]

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
