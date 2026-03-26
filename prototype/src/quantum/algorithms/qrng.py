from quantum.device import QuantumDevice
from quantum.state import QState

def qrng(device: QuantumDevice, map: dict[QState, int]) -> int:
    with device.alloc() as psi:
        psi.hadamard()
        psi, measurment = psi.measure()
    return map[measurment]
