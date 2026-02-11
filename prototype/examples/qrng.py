from typing import Callable
from quantum.qubit import Qubit, QuantumState, KET_0, KET_1
from quantum.device import QuantumDevice

def qrng(device: QuantumDevice, bitmap: Callable[[QuantumState], int]) -> int:
    psi: Qubit # Yo why doesn't type hinting work!
    with device.qalloc() as psi:
        psi.hadamard()
        measurement = psi.measure()
    return bitmap(measurement)

def main():
    def bitmap(x: QuantumState) -> int:
        if x == KET_0:
            return 0
        elif x == KET_1:
            return 1
        else:
            raise Exception("Invalid Quantum State in Bitmap")

    device = QuantumDevice(4)
    qrng(device, bitmap)
        

if __name__ == "__main__":
    main()
