from quantum.viz import Visualizer
from typing import Callable, IO
from quantum.qubit import Qubit
from quantum.state import QuantumState, KET_0, KET_1
from quantum.device import QuantumDevice
from utils.data import open_csv

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

    with open_csv('./output/data.csv') as datafile:
        device = QuantumDevice(4, log=datafile, visualize=True)
        result = [qrng(device, bitmap) for _ in range(16)]
        visualizer = Visualizer()
        anim = visualizer.generate_animation(device.history)
        anim.save("output/qrng.mp4", writer='ffmpeg')
    print(result)

if __name__ == "__main__":
    main()
