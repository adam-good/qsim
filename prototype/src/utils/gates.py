from utils.typing import matrix
import quantum.state as qstate
import numpy as np
import numpy.typing as npt

type qgate = matrix

def _apply_gate(psi: qstate.state, gate: qgate) -> qstate.state:
    if not _is_unitary(gate):
        raise Exception("Gate Must be a Unitary Matrix")

    return gate @ psi

def hadamard(psi: qstate.state) -> qstate.state:
    gate = np.matrix(
        [[1,1],
        [1,-1]]
    ) / np.sqrt(2)
    return gate @ psi

def xgate(psi: qstate.state) -> qstate.state:
    gate = np.matrix(
        [[0,1],
        1,0]
    )
    return gate @ psi

def negate(psi: qstate.state) -> qstate.state:
    return xgate(psi)


def _is_square(matrix: npt.NDArray) -> bool:
    return len(matrix.shape) == 2 and matrix.shape[0] == matrix.shape[1]

def _is_unitary(matrix: npt.NDArray) -> bool:
        if not _is_square(matrix):
            return False
                
        identity = np.identity(matrix.shape[0])
        # TODO: Add the conjugate part when we upgrade to complex numbers
        conj_transpose = matrix.transpose()

        return np.allclose(matrix @ conj_transpose, identity)
    

