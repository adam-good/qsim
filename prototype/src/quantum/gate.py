import dataclasses
import quantum.state as qst
import utils.math.matrix as matrix
from enum import Enum


@dataclasses.dataclass(frozen=True)
class QGate:
    matrix: matrix.Matrix

    # TODO: Find a way to not run this check for every new gate instance
    def __post_init__(self):
        if not matrix.is_unitary(self.matrix):
            raise ValueError("Quantum Gate Matrix Must Be Unitary")


class Gates(Enum):
    H = 0
    X = 1


_hadamard_matrix = matrix.Matrix(((1, 1), (1, -1))) * qst.HADAMARD_CONST
_negate_matrix = matrix.Matrix(((0, 1), (1, 0)))
COMMON_GATES: dict[Gates, QGate] = {
    Gates.H: QGate(_hadamard_matrix),
    Gates.X: QGate(_negate_matrix),
}


def apply_gate(psi: qst.QState, gate: QGate) -> qst.QState:
    return qst.QState(gate.matrix @ psi.vector)


def compose_gates(g1: QGate, g2: QGate) -> QGate:
    return QGate(g1.matrix @ g2.matrix)


def hgate(psi: qst.QState) -> qst.QState:
    gate: QGate = COMMON_GATES[Gates.H]
    return apply_gate(psi, gate)


def xgate(psi: qst.QState) -> qst.QState:
    gate: QGate = COMMON_GATES[Gates.X]
    return apply_gate(psi, gate)
