from utils.typing import matrix
import quantum.state as qstate
import numpy as np

type qgate = matrix

def apply_gate(psi: qstate.state, gate: qgate, check_unitary: bool = True) -> qstate.state:
    if check_unitary and not _is_unitary(gate):
        raise Exception("Gate is Not Unitary")
    return gate @ psi

def hadamard(psi: qstate.state) -> qstate.state:
    gate: qgate = np.matrix(
        [[1,1],
        [1,-1]]
    ) / np.sqrt(2)   
    return apply_gate(psi, gate, check_unitary=False)

def xgate(psi: qstate.state) -> qstate.state:
    gate = np.matrix(
        [[0,1],
        1,0]
    )
    return apply_gate(psi, gate, check_unitary=False)

def negate(psi: qstate.state) -> qstate.state:
    return xgate(psi)


def _is_square(mat: matrix) -> bool:
    return len(mat.shape) == 2 and mat.shape[0] == mat.shape[1]

def _is_unitary(mat: matrix) -> bool:
        if not _is_square(mat):
            return False
                
        identity = np.identity(mat.shape[0])
        # TODO: Add the conjugate part when we upgrade to complex numbers
        conj_transpose = mat.transpose()

        return np.allclose(mat @ conj_transpose, identity)
    

