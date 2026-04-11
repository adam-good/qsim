import time
import utils.channel as chnl
import quantum.state as qst
import quantum.device as qdev
import quantum.algorithms.random as qrand

# TODO: This file needs to be made more simple
# TODO: Expand to work in batches instead of single qubits
# TODO: Privacy Amplification Algorithms???
# TODO: Add Unit Tests!!!

DEFAULT_BASIS_MAP: dict[int, qst.QBasis] = {0:qst.Z_BASIS, 1:qst.X_BASIS}
DEFAULT_VAL_MAP: dict[qst.QState, int] = {
    qst.KET0:0,
    qst.KET1:1,
    qst.KETPLUS:0,
    qst.KETMINUS:1
}

def _bb84_encode(
    device: qdev.QuantumDevice, val: int, basis_key: int
) -> tuple[qdev.Qubit, int]:
    with device.alloc() as qubit:
        match (basis_key, val):
            case (0, 0):
                qubit = qubit  # KET0
            case (0, 1):
                qubit = qubit.negate()  # KET1
            case (1, 0):
                qubit = qubit.hadamard()  # KET PLUS
            case (1, 1):
                qubit = qubit.negate().hadamard()  # KET MINUS
        return (device.copy(qubit), basis_key)


def _bb84_decode(
    device: qdev.QuantumDevice,
    qubit: qdev.Qubit,
    basis_key: int,
    basis_map: dict[int, qst.QBasis] = DEFAULT_BASIS_MAP,
    value_map: dict[qst.QState, int] = DEFAULT_VAL_MAP
) -> tuple[int, int]:
    basis = basis_map[basis_key]
    qubit, state = qubit.measure(basis)
    val = value_map[state]
    return (val, basis_key)


# NOTE: This seems unnecesary.
#       Leaving for now because I anticipate adding compleixty later
def _bb84_send_qubit(qubit: qdev.Qubit, channel: chnl.ChannelEndpoint[qdev.Qubit]):
    chnl.send(channel, qubit)


def _bb84_exchange_basis(basis_key: int, channel: chnl.ChannelEndpoint[int]) -> int:
    remote_basis_key = chnl.recv(channel)
    chnl.send(channel, basis_key)
    return remote_basis_key


def bb84_send(
    device: qdev.QuantumDevice,
    key: list[int],
    n_bits: int,
    quantum_channel: chnl.ChannelEndpoint[qdev.Qubit],
    auth_channel: chnl.ChannelEndpoint[int],
):
    assert len(key) == n_bits  # NOTE: Is this good practice?

    idx = 0
    while idx < n_bits:
        basis_key = qrand.random_bit(device)
        qubit, local_basis_key = _bb84_encode(device, key[idx], basis_key)
        _bb84_send_qubit(qubit, quantum_channel)
        remote_basis_key = _bb84_exchange_basis(basis_key, auth_channel)

        if local_basis_key == remote_basis_key:
            idx += 1


def bb84_recv(
    device: qdev.QuantumDevice,
    n_bits: int,
    primary_channel: chnl.ChannelEndpoint[qdev.Qubit],
    auth_channel: chnl.ChannelEndpoint[int],
    verbose=False,
) -> list[int]:
    key: list[int | None] = n_bits * [None]
    idx = 0
    while idx < n_bits:
        qubit = chnl.recv(primary_channel)
        basis_key = qrand.random_bit(device)
        val, local_basis_key = _bb84_decode(device, qubit, basis_key)

        chnl.send(auth_channel, local_basis_key)
        remote_basis_key = chnl.recv(auth_channel)

        if local_basis_key == remote_basis_key:
            key[idx] = val
            idx += 1

        if verbose:
            time.sleep(0.1)
            print(
                f"Data: {''.join([str(k) if k is not None else ' ' for k in key])}",
                end="\r",
            )
    if verbose:
        print("")
    return [k for k in key if k]
