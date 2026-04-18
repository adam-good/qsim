from src.quantum.state import Z_BASIS
import dataclasses
import time
import utils.channel as chnl
import utils.math.bit as binary
import quantum.state as qst
import quantum.gate as qgt
import quantum.device as qdev
import quantum.algorithms.random as qrand
import enum

# TODO: This file needs to be made more simple
# TODO: Expand to work in batches instead of single qubits
# TODO: Privacy Amplification Algorithms???
# TODO: Add Unit Tests!!!

class BB84Basis(enum.Enum):
    RECTLINEAR = enum.auto()
    DIAGONAL = enum.auto()

@dataclasses.dataclass(frozen=True)
class BB84Input:
    bit: binary.Bit
    basis: BB84Basis
    qubit: qdev.Qubit

@dataclasses.dataclass(frozen=True)
class BB84Encoding:
    qubit: qdev.Qubit

# TODO: How am I going to actually implement this?
#       I must act as an in between for the local and remote
@dataclasses.dataclass(frozen=True)
class BB84QuantumTransmission:
    encoding: BB84Encoding
    ...

@dataclasses.dataclass(frozen=True)
class BB84Decoder:
    qubit: qdev.Qubit
    basis: BB84Basis

@dataclasses.dataclass
class BB84Decoding:
    bit: binary.Bit

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

