import utils.typing as types
import quantum.state as qstate
import numpy as np

type QGate = types.Matrix

def apply_gate(psi: qstate.QState, gate: QGate, check_unitary: bool = True) -> qstate.QState:
    if check_unitary and not _is_unitary(gate):
        raise Exception("Gate is Not Unitary")
    return gate @ psi

def hadamard(psi: qstate.QState) -> qstate.QState:
    gate: QGate = types.Matrix(
        ((1,1),
        (1,-1))
    ) / np.sqrt(2)   
    return apply_gate(psi, gate, check_unitary=False)

def xgate(psi: qstate.QState) -> qstate.QState:
    gate: QGate = types.Matrix(
        ((0,1),
         (1,0))
    )
    return apply_gate(psi, gate, check_unitary=False)

def negate(psi: qstate.QState) -> qstate.QState:
    return xgate(psi)


def _is_square(mat: types.Matrix) -> bool:
    return len(mat.shape) == 2 and mat.shape[0] == mat.shape[1]

def _is_unitary(mat: types.Matrix) -> bool:
        if not _is_square(mat):
            return False
                
        identity = types.Matrix.identity(mat.shape[0])
        # TODO: Add the conjugate part when we upgrade to complex numbers
        conj_transpose = mat.transpose

        return mat @ conj_transpose == identity
    

