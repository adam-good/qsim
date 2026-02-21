from typing import Callable, IO
from quantum.qubit import Qubit, QuantumState, KET_0, KET_1
from quantum.device import QuantumDevice

def qrng(device: QuantumDevice, bitmap: Callable[[QuantumState], int], logging: IO | None = None) -> int:
    psi: Qubit # Yo why doesn't type hinting work!
    with device.qalloc() as psi:
        psi.hadamard()
        if logging:
            logging.write(psi.to_csv_form())
        measurement = psi.measure()
        if logging:
            logging.write(psi.to_csv_form())
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
    with open("output/data.csv", "w") as datafile:
        result = [qrng(device, bitmap, datafile) for _ in range(16)]
    print(result)
        

if __name__ == "__main__":
    main()
