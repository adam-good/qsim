from typing import Callable
from quantum.qubit import Qubit
from quantum.state import QuantumState, KET_0, KET_1
from quantum.device import QuantumDevice
from utils.data import open_csv

def qrng(n: int, device: QuantumDevice, bitmap: Callable[[QuantumState], int]) -> int:
    for psi in device.qalloc():
        psi.hadamard()
        measure
    # psi: Qubit # Yo why doesn't type hinting work!
    # with device.qalloc() as psi:
    #     psi.hadamard()
    #     measurement = psi.measure()
    # return bitmap(measurement)

def main():
    def bitmap(x: QuantumState) -> int:
        if x == KET_0:
            return 0
        elif x == KET_1:
            return 1
        else:
            raise Exception("Invalid Quantum State in Bitmap")

    n_qubits = 4

    with open_csv('./output/data.csv') as datafile:
        device = QuantumDevice(n_qubits, log=datafile, visualize=True)
        result = qrng(16, device, bitmap) #[qrng(device, bitmap) for _ in range(64)]
        anim = device.generate_animation()
        anim.save("output/qrng.mp4", writer="ffmpeg")
    print(result)

if __name__ == "__main__":
    main()
