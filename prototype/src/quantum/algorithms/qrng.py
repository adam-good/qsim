from quantum.device import QuantumDevice
from quantum.state import QState, Z_BASIS

def qrng(device: QuantumDevice, map: dict[QState, int]) -> list[int]:
    with device.alloc() as psi:
        psi.hadamard()
        psi, measurment = psi.measure(Z_BASIS)
    return [map[measurment]]
