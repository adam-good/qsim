import functools
import typing
import dataclasses
import enum
import quantum.state as qst
import utils.math.matrix as matrix


@dataclasses.dataclass(frozen=True)
class QGate:
    matrix: matrix.Matrix

    # TODO: Find a way to not run this check for every new gate instance
    def __post_init__(self):
        if not matrix.is_unitary(self.matrix):
            raise ValueError("Quantum Gate Matrix Must Be Unitary")

    @typing.overload
    def __matmul__(self, other: QGate) -> QGate: ...  # Gate Composition
    @typing.overload
    def __matmul__(self, other: qst.QState) -> qst.QState: ...  # Gate Application
    def __matmul__(self, other: QGate | qst.QState) -> QGate | qst.QState:
        if isinstance(other, QGate):
            return compose_gates([self, other])
        elif isinstance(other, qst.QState):
            return apply_gate(self, other)
        else:
            return NotImplemented


class Gates(enum.Enum):
    I = enum.auto()
    H = enum.auto()
    X = enum.auto()

_identity_matrix = matrix.identity(2)
_hadamard_matrix = matrix.Matrix(((1, 1), (1, -1))) * qst.HADAMARD_CONST
_negate_matrix = matrix.Matrix(((0, 1), (1, 0)))

I_GATE = QGate(_identity_matrix)
H_GATE = QGate(_hadamard_matrix)
X_GATE = QGate(_negate_matrix)
COMMON_GATES: dict[Gates, QGate] = {
    Gates.I: I_GATE,
    Gates.H: H_GATE,
    Gates.X: X_GATE,
}


def apply_gate(gate: QGate, psi: qst.QState) -> qst.QState:
    return qst.QState(gate.matrix @ psi.vector)


def compose_gates(gates: list[QGate]) -> QGate:
    def _compose_gates(g1: QGate, g2: QGate) -> QGate:
        return QGate(g1.matrix @ g2.matrix)

    return functools.reduce(_compose_gates, gates)
