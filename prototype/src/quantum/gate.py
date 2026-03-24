import math
import utils.typing as types
import quantum.state as qstate
from enum import Enum

QGate = types.Matrix

class Gates(Enum):
    H = 0
    X = 1

COMMON_GATES: dict[Gates, QGate] = {
    Gates.H: QGate( ((1,1),(1,-1)) ) / math.sqrt(2),
    Gates.X: QGate( ((0,1),(1,0)) )
}

def apply_gate(psi: qstate.QState, gate: QGate, check_unitary: bool = True) -> qstate.QState:
    if check_unitary and not gate.is_unitary():
        raise Exception("Gate is Not Unitary")
    return gate @ psi

def hgate(psi: qstate.QState) -> qstate.QState:
    gate: QGate = COMMON_GATES[Gates.H]
    return apply_gate(psi, gate, check_unitary=False)

def xgate(psi: qstate.QState) -> qstate.QState:
    gate: QGate = COMMON_GATES[Gates.X]
    return apply_gate(psi, gate, check_unitary=False)

hadamard  = hgate
negate = xgate

h = hgate
x = xgate    

