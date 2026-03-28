import utils.channel as chnl
from quantum.state import QBasis, QState, Z_BASIS, X_BASIS, KET0, KET1
from quantum.device import QuantumDevice, Qubit
from quantum.algorithms.qrng import qrng

def _bb84_encode(device: QuantumDevice, val: int) -> tuple[Qubit,int]:
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
        return (qubit, basis)

def _bb84_decode(
    device: QuantumDevice,
    qubit: Qubit,
    basis_map: dict[int, QBasis] = {0:Z_BASIS, 1:X_BASIS},
    value_map: dict[QState, int] = {KET0:0, KET1:1}) -> tuple[int, int]:
    basis_key = qrng(device)
    basis = basis_map[basis_key]
    qubit, state = qubit.measure(basis)
    val = value_map[state]
    return (val, basis_key)
    

def bb84_send(
    device: QuantumDevice,
    key: list[int],
    n_bits: int,
    quantum_channel: chnl.ChannelEndpoint[Qubit],
    auth_channel: chnl.ChannelEndpoint[int]):
    assert len(key) == n_bits # NOTE: Is this good practice?

    idx = 0
    while idx < n_bits:
        qubit, local_basis_key = _bb84_encode(device, key[idx])

        chnl.send(quantum_channel, qubit)
        remote_basis_key = chnl.recv(auth_channel)
        chnl.send(auth_channel, local_basis_key)

        if local_basis_key == remote_basis_key:
            idx += 1

def bb84_recv(
    device: QuantumDevice,
    n_bits: int,
    primary_channel: chnl.ChannelEndpoint[Qubit],
    auth_channel: chnl.ChannelEndpoint[int],
    verbose=False) -> list[int]:
    key: list[int] = n_bits*[0]
    idx = 0
    while idx < n_bits:
        qubit = chnl.recv(primary_channel)
        val, local_basis_key = _bb84_decode(device, qubit)

        chnl.send(auth_channel, local_basis_key)
        remote_basis_key = chnl.recv(auth_channel)

        if local_basis_key == remote_basis_key:
            key[idx] = val
            idx += 1

        if verbose:
            print(f"Data: {key}", end='\r')
    if verbose:
        print("")
    return key

