import utils.channel as chnl
import quantum.state as qst
import quantum.device as qdev
from quantum.algorithms.qrng import qrng

def _bb84_encode(device: qdev.QuantumDevice, val: int) -> tuple[qdev.Qubit,int]:
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
    device: qdev.QuantumDevice,
    qubit: qdev.Qubit,
    basis_map: dict[int, qst.QBasis] = {0:qst.Z_BASIS, 1:qst.X_BASIS},
    value_map: dict[qst.QState, int] = {qst.KET0:0, qst.KET1:1}) -> tuple[int, int]:
    basis_key = qrng(device)
    basis = basis_map[basis_key]
    qubit, state = qubit.measure(basis)
    val = value_map[state]
    return (val, basis_key)
    

def bb84_send(
    device: qdev.QuantumDevice,
    key: list[int],
    n_bits: int,
    quantum_channel: chnl.ChannelEndpoint[qdev.Qubit],
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
    device: qdev.QuantumDevice,
    n_bits: int,
    primary_channel: chnl.ChannelEndpoint[qdev.Qubit],
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

