import dataclasses
import utils.channel as chnl
import utils.math.bit as binary
import quantum.state as qst
import quantum.gate as qgt
import quantum.device as qdev
import enum

# TODO: This file needs to be made more simple
# TODO: Expand to work in batches instead of single qubits
# TODO: Privacy Amplification Algorithms???
# TODO: Add Unit Tests!!!


class BB84Basis(enum.Enum):
    RECTLINEAR = enum.auto()
    DIAGONAL = enum.auto()

class BB84Result(enum.Enum):
    SUCCESS = True
    FAILURE = False

@dataclasses.dataclass
class BasisBitPair:
    basis: BB84Basis
    bit: binary.Bit

@dataclasses.dataclass
class BasisQubitPair:
    basis: BB84Basis
    qubit: qdev.Qubit


DEFAULT_BASIS_MAP: dict[BB84Basis, qst.QBasis] = {
    BB84Basis.RECTLINEAR:qst.Z_BASIS,
    BB84Basis.DIAGONAL:qst.X_BASIS
}

DEFAULT_VAL_MAP: dict[qst.QState, binary.Bit] = {
    qst.KET0: binary.BIT_0,
    qst.KET1: binary.BIT_1,
    qst.KETPLUS: binary.BIT_0,
    qst.KETMINUS: binary.BIT_1,
}

DEFAULT_ENCODING_OPS: dict[BasisBitPair, qgt.QGate] = {
    BasisBitPair(BB84Basis.RECTLINEAR, binary.BIT_0) : qgt.I_GATE, # I|0⟩ = |0⟩
    BasisBitPair(BB84Basis.RECTLINEAR, binary.BIT_1) : qgt.X_GATE, # X|0⟩
    BasisBitPair(BB84Basis.DIAGONAL, binary.BIT_0)   : qgt.H_GATE, # H|0⟩
    BasisBitPair(BB84Basis.DIAGONAL, binary.BIT_1)   : qgt.compose_gates([qgt.H_GATE, qgt.X_GATE]) # HX|0⟩
}

@dataclasses.dataclass
class BB84Config:
    basis_map: dict[BB84Basis, qst.QBasis] = DEFAULT_BASIS_MAP
    value_map: dict[qst.QState, binary.Bit] = DEFAULT_VAL_MAP
    ops: dict[BasisBitPair, qgt.QGate] = DEFAULT_ENCODING_OPS

@dataclasses.dataclass(frozen=True)
class BB84Encoder:
    config: BB84Config
    device: qdev.QuantumDevice
    qubit: qdev.Qubit
    pair: BasisBitPair # NOTE: Should pair be part of this?

    def __post__init(self):
        # TODO: self.qubit not in self.device
        if self.qubit.ref_id not in self.device.qubits.keys():
            raise ValueError(f"BB84Encoder Configured With Foreign Qubit {self.qubit}")

@dataclasses.dataclass(frozen=True)
class BB84Encoding:
    pair: BasisBitPair
    qubit: qdev.Qubit

@dataclasses.dataclass(frozen=True)
class BB84QuantumTransmitter:
    device: qdev.QuantumDevice
    channel: chnl.Channel[qdev.Qubit]
    encoding: BB84Encoding | None

@dataclasses.dataclass(frozen=True)
class BB84BasisTransmitter:
    channel: chnl.Channel[BB84Basis]
    basis: BB84Basis | None

@dataclasses.dataclass(frozen=True)
class BB84QuantumReciever:
    device: qdev.QuantumDevice
    channel: chnl.Channel[qdev.Qubit]

@dataclasses.dataclass(frozen=True)
class BB84Decoder:
    config: BB84Config
    device: qdev.QuantumDevice
    pair: BasisQubitPair

    def __post__init(self):
        # TODO: self.pair.qubit not in self.device
        if self.pair.qubit.ref_id not in self.device.qubits.keys():
            raise ValueError(f"BB84Decoder Configured With Foreign Qubit: {self.pair.qubit}")
    

@dataclasses.dataclass(frozen=True)
class BB84Decoding:
    pair: BasisQubitPair
    bit: binary.Bit

@dataclasses.dataclass(frozen=True)
class BB84BasisPair:
    basis1: BB84Basis
    basis2: BB84Basis
    

def bb84_encode(encoder: BB84Encoder) -> BB84Encoding:
    qubit: qdev.Qubit = encoder.device.prepare_single_qubit(
                        qubit=encoder.qubit,
                        gate=encoder.config.ops[encoder.pair]
                    )
    return BB84Encoding(encoder.pair, qubit)

# TODO: This does not need to be a BB84 function
#       I should implement sending and recieving operations on devices
# TODO: Make this recursive once BB84Transmitter is vectorized
def bb84_transmit_qubit(transmitter: BB84QuantumTransmitter) -> BB84QuantumTransmitter:
    if transmitter.encoding is None:
        return transmitter
    free_qubit = transmitter.device.pop_qubit(transmitter.encoding.qubit)
    channel = chnl.send(transmitter.channel, free_qubit)
    return BB84QuantumTransmitter(transmitter.device, channel, None)


def bb84_recieve_qubit(reciever: BB84QuantumReciever) -> tuple[qdev.Qubit | None, BB84QuantumReciever]:
    qubit, channel = chnl.recv(reciever.channel)
    if qubit is None:
        return None,reciever
    reciever.device.push_qubit(qubit)
    return qubit, BB84QuantumReciever(reciever.device, channel)

def bb84_decode(decoder: BB84Decoder) -> BB84Decoding:
    measurement: qst.QState = decoder.device.measure_single_qubit(
                                qubit=decoder.pair.qubit,
                                basis=decoder.config.basis_map[decoder.pair.basis])
    return BB84Decoding(decoder.pair, decoder.config.value_map[measurement])

def bb84_transmit_basis(transmitter: BB84BasisTransmitter) -> BB84BasisTransmitter:
    if transmitter.basis is None:
        return transmitter
    return BB84BasisTransmitter(
        chnl.send(transmitter.channel, transmitter.basis),
        None
    )

# def bb84_validate(basis: BB84BasisPair) -> BB84Result:
#     return BB84Result(basis.basis1 == basis.basis2)
