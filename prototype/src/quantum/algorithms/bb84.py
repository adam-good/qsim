from queue import Queue
from quantum.device import QuantumDevice, Qubit
from quantum.algorithms.qrng import qrng

def _bb84_encode(device: QuantumDevice, val: int) -> Qubit:
    basis = qrng(device)
    with device.alloc() as qubit:
        match (basis, val):
            case (0, 0):
                qubit = qubit
            case (0, 1):
                qubit = qubit.negate()
            case (1, 0):
                qubit = qubit.hadamard()
            case (1, 1):
                qubit = qubit.negate().hadamard()
        return qubit
    

def bb84_send(
    device: QuantumDevice,
    key: list[int],
    primary_channel: Queue, auth_channel: Queue):

    qubit = _bb84_encode(device, key[0])
    primary_channel.put(qubit)
    
    
def bb84_recv(device: QuantumDevice, primary_channel: Queue, auth_channel: Queue) -> list[int]:
    return []
