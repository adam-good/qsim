import dataclasses
import math
import quantum.state as qst
import utils.math.matrix as matrix
from enum import Enum

@dataclasses.dataclass(frozen=True)
class QGate:
    matrix: matrix.Matrix

class Gates(Enum):
    H = 0
    X = 1


COMMON_GATES: dict[Gates, QGate] = {
    Gates.H: QGate(((1, 1), (1, -1))) / math.sqrt(2),
    Gates.X: QGate(((0, 1), (1, 0))),
}


def apply_gate(psi: qst.QState, gate: QGate, check_unitary: bool = True) -> qst.QState:
    if check_unitary and not gate.is_unitary():
        raise Exception("Gate is Not Unitary")
    return qst.qstate_from_vector(gate @ psi)


def hgate(psi: qst.QState) -> qst.QState:
    gate: QGate = COMMON_GATES[Gates.H]
    return apply_gate(psi, gate, check_unitary=False)


def xgate(psi: qst.QState) -> qst.QState:
    gate: QGate = COMMON_GATES[Gates.X]
    return apply_gate(psi, gate, check_unitary=False)


hadamard = hgate
negate = xgate

h = hgate
x = xgate
