from quantum.device import QuantumDevice
from quantum.state import QState, Z_BASIS, KET0, KET1

def qrng(device: QuantumDevice, map: dict[QState, int] = {KET0:0, KET1:1}) -> int:
    with device.alloc() as psi:
        psi.hadamard()
        psi, measurment = psi.measure(Z_BASIS)
    return map[measurment]
