import dataclasses
import utils.comms.channel as chnl
import utils.math.bit as binary
import quantum.state as qst
import quantum.gate as qgt
import quantum.device as qdev
import enum

# TODO: This file needs to be made more simple
# TODO: Expand to work in batches instead of single qubits
# TODO: Privacy Amplification Algorithms???
# TODO: Add Unit Tests!!!

@dataclasses.dataclass(frozen=True)
class Key:
    bits: list[binary.Bit | None]
    
    def __repr__(self):
        return "".join( ('-' if k is None else str(k) for k in self.bits) )

class Basis(enum.Enum):
    RECTLINEAR = enum.auto()
    DIAGONAL = enum.auto()

class Result(enum.Enum):
    SUCCESS = True
    FAILURE = False

@dataclasses.dataclass
class BasisBitPair:
    basis: Basis
    bit: binary.Bit

@dataclasses.dataclass
class BasisQubitPair:
    basis: Basis
    qubit: qdev.Qubit


DEFAULT_BASIS_MAP: dict[Basis, qst.QBasis] = {
    Basis.RECTLINEAR:qst.Z_BASIS,
    Basis.DIAGONAL:qst.X_BASIS
}

DEFAULT_VAL_MAP: dict[qst.QState, binary.Bit] = {
    qst.KET0: binary.BIT_0,
    qst.KET1: binary.BIT_1,
    qst.KETPLUS: binary.BIT_0,
    qst.KETMINUS: binary.BIT_1,
}

DEFAULT_ENCODING_OPS: dict[BasisBitPair, qgt.QGate] = {
    BasisBitPair(Basis.RECTLINEAR, binary.BIT_0) : qgt.I_GATE, # I|0⟩ = |0⟩
    BasisBitPair(Basis.RECTLINEAR, binary.BIT_1) : qgt.X_GATE, # X|0⟩
    BasisBitPair(Basis.DIAGONAL, binary.BIT_0)   : qgt.H_GATE, # H|0⟩
    BasisBitPair(Basis.DIAGONAL, binary.BIT_1)   : qgt.compose_gates([qgt.H_GATE, qgt.X_GATE]) # HX|0⟩
}

@dataclasses.dataclass
class Config:
    basis_map: dict[Basis, qst.QBasis] = DEFAULT_BASIS_MAP
    value_map: dict[qst.QState, binary.Bit] = DEFAULT_VAL_MAP
    ops: dict[BasisBitPair, qgt.QGate] = DEFAULT_ENCODING_OPS

@dataclasses.dataclass(frozen=True)
class Encoder:
    config: Config
    device: qdev.QuantumDevice
    qubit: qdev.Qubit
    
@dataclasses.dataclass(frozen=True)
class Encoding:
    qubit: qdev.Qubit

@dataclasses.dataclass(frozen=True)
class QuantumTransmitter:
    device: qdev.QuantumDevice
    channel: chnl.Channel[qdev.Qubit]

@dataclasses.dataclass(frozen=True)
class BasisTransmitter:
    channel: chnl.Channel[Basis]
    basis: Basis | None

@dataclasses.dataclass(frozen=True)
class QuantumReciever:
    device: qdev.QuantumDevice
    channel: chnl.Channel[qdev.Qubit]

@dataclasses.dataclass(frozen=True)
class BasisReciever:
    channel: chnl.Channel[Basis]

@dataclasses.dataclass(frozen=True)
class Decoder:
    config: Config
    device: qdev.QuantumDevice

@dataclasses.dataclass(frozen=True)
class Decoding:
    bit: binary.Bit

@dataclasses.dataclass(frozen=True)
class BasisPair:
    basis1: Basis
    basis2: Basis
    

def encode(encoder: Encoder, data: BasisBitPair) -> Encoding:
    qubit: qdev.Qubit = encoder.device.prepare_single_qubit(
                        qubit=encoder.qubit,
                        gate=encoder.config.ops[data]
                    )
    return Encoding(qubit)

# TODO: This does not need to be a BB84 function
#       I should implement sending and recieving operations on devices
# TODO: Make this recursive once BB84Transmitter is vectorized
def transmit_qubit(transmitter: QuantumTransmitter, qubit: qdev.Qubit) -> QuantumTransmitter:
    free_qubit = transmitter.device.pop_qubit(qubit)
    transmitter.channel.send(free_qubit)
    return QuantumTransmitter(transmitter.device, transmitter.channel)


def recieve_qubit(reciever: QuantumReciever) -> tuple[qdev.Qubit, QuantumReciever]:
    qubit = reciever.channel.recv()
    reciever.device.push_qubit(qubit)
    return qubit, QuantumReciever(reciever.device, reciever.channel)

def decode(decoder: Decoder, data: BasisQubitPair) -> Decoding:
    measurement: qst.QState = decoder.device.measure_single_qubit(
                                qubit=data.qubit,
                                basis=decoder.config.basis_map[data.basis])
    return Decoding(decoder.config.value_map[measurement])

def transmit_basis(transmitter: BasisTransmitter) -> BasisTransmitter:
    if transmitter.basis is None:
        return transmitter
    return BasisTransmitter(
        transmitter.channel.send(transmitter.basis),
        None
    )

def recv_basis(reciever: BasisReciever) -> tuple[Basis, BasisReciever]:
    basis = reciever.channel.recv()
    return basis,reciever

def validate_basis(basis: BasisPair) -> Result:
    return Result(basis.basis1 == basis.basis2)
