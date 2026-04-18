import time
import utils.channel as chnl
import utils.math.bit as bit
import quantum.state as qst
import quantum.gate as qgt
import quantum.device as qdev
import quantum.algorithms.random as qrand

# TODO: This file needs to be made more simple
# TODO: Expand to work in batches instead of single qubits
# TODO: Privacy Amplification Algorithms???
# TODO: Add Unit Tests!!!
# TODO: Use the bit type

DEFAULT_BASIS_MAP: dict[bit.Bit, qst.QBasis] = {bit.BIT_0: qst.Z_BASIS, bit.BIT_1: qst.X_BASIS}
DEFAULT_VAL_MAP: dict[qst.QState, bit.Bit] = {
    qst.KET0: bit.BIT_0,
    qst.KET1: bit.BIT_1,
    qst.KETPLUS: bit.BIT_0,
    qst.KETMINUS: bit.BIT_1,
}

ENCODE_OPS: dict[tuple[bit.Bit, bit.Bit], qgt.QGate] = {
    (bit.BIT_0, bit.BIT_0): qgt.I_GATE,
    (bit.BIT_0, bit.BIT_1): qgt.X_GATE,
    (bit.BIT_1, bit.BIT_0): qgt.H_GATE,
    (bit.BIT_1, bit.BIT_1): qgt.compose_gates([qgt.H_GATE, qgt.X_GATE])
}


def _bb84_encode(
    device: qdev.QuantumDevice, qubit: qdev.Qubit, val: bit.Bit, basis_key: bit.Bit
) -> tuple[qdev.Qubit, bit.Bit]:
    gate = ENCODE_OPS[(val, basis_key)]
    qubit = device.prepare_single_qubit(qubit, gate)
    return (device.pop_qubit(qubit), basis_key)


def _bb84_decode(
    device: qdev.QuantumDevice,
    qubit: qdev.Qubit,
    basis_key: bit.Bit,
    basis_map: dict[bit.Bit, qst.QBasis] = DEFAULT_BASIS_MAP,
    value_map: dict[qst.QState, bit.Bit] = DEFAULT_VAL_MAP,
) -> tuple[bit.Bit, bit.Bit]:
    basis = basis_map[basis_key]
    state = device.measure_single_qubit(qubit, basis)
    val = value_map[state]
    return (val, basis_key)


def bb84_send(
    device: qdev.QuantumDevice,
    key: list[bit.Bit],
    n_bits: int,
    quantum_channel: chnl.ChannelEndpoint[qdev.Qubit],
    auth_channel: chnl.ChannelEndpoint[int],
):
    assert len(key) == n_bits  # NOTE: Is this good practice?

    idx = 0
    while idx < n_bits:
        basis_key = qrand.random_bit(device)
        with device.alloc_single() as qubit:
            qubit, local_basis_key = _bb84_encode(device, qubit, key[idx], basis_key)
            qubit = device.pop_qubit(qubit)
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
    verbose=False,
) -> list[int]:
    key: list[int | None] = n_bits * [None]
    idx = 0
    while idx < n_bits:
        basis_key = qrand.random_bit(device)
        qubit = chnl.recv(primary_channel)
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
