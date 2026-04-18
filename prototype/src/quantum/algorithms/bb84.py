import dataclasses
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

@dataclasses.dataclass(frozen=True)
class BB84EncoderInput:
    bit: binary.Bit
    basis: BB84Basis
    qubit: qdev.Qubit

@dataclasses.dataclass(frozen=True)
class BB84Encoding:
    qubit: qdev.Qubit

@dataclasses.dataclass(frozen=True)
class BB84DecoderInput:
    qubit: qdev.Qubit
    basis: BB84Basis

@dataclasses.dataclass
class BB84Decoding:
    bit: binary.Bit

@dataclasses.dataclass(frozen=True)
class BB84BasisPair:
    basis1: BB84Basis
    basis2: BB84Basis

# TODO: How am I going to actually implement transmissions?
#       I must act as an in between for the local and remote

@dataclasses.dataclass(frozen=True)
class BB84QuantumTransmission:
    qubit: qdev.Qubit
    
@dataclasses.dataclass(frozen=True)
class BB84Transmission:
    basis: BB84Basis

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
    device: qdev.QuantumDevice 

def bb84_encode(config: BB84Config, input: BB84EncoderInput) -> BB84Encoding:
    psi = config.device.prepare_single_qubit(
                        qubit=input.qubit,
                        gate=config.ops[BasisBitPair(input.basis, input.bit)]
                )
    return BB84Encoding(qubit=psi)

def bb84_transmit_encoding(config: BB84Config, encoding: BB84Encoding) -> BB84QuantumTransmission:
    return BB84QuantumTransmission(config.device.pop_qubit(encoding.qubit))

def bb84_recieve_encoding(config: BB84Config, transmission:BB84QuantumTransmission) -> BB84Encoding:
    config.device.push_qubit(transmission.qubit) # TODO: This should return a qubit for work to be done
    return BB84Encoding(transmission.qubit)

def bb84_construct_decoder(config: BB84Config, encoding: BB84Encoding, basis: BB84Basis) -> BB84DecoderInput:
    return BB84DecoderInput(encoding.qubit, basis)

def bb84_decode(config: BB84Config, input: BB84DecoderInput) -> binary.Bit:
    measurement: qst.QState = config.device.measure_single_qubit(
                                qubit=input.qubit,
                                basis=config.basis_map[input.basis])
    return config.value_map[measurement]

def bb84_transmit_basis(
    basis: BB84Basis,
    transmission: BB84Transmission) -> BB84BasisPair: # TODO: How should this be implemented?
    return BB84BasisPair(basis, transmission.basis)

def bb84_validate(basis: BB84BasisPair) -> BB84Result:
    return BB84Result(basis.basis1 == basis.basis2)
