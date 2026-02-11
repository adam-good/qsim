import numpy as np
import numpy.typing as npt

H_GATE: npt.NDArray[np.float64] = np.array(
            [[1, 1],
             [1,-1]] / np.sqrt(2)
         )
X_GATE: npt.NDArray[np.float64] = np.array(
    [[0, 1],
     [1, 0]]
)

def is_square(matrix: npt.NDArray) -> bool:
    return len(matrix.shape) == 2 and matrix.shape[0] == matrix.shape[1]

def is_unitary(matrix: npt.NDArray) -> bool:
        if not is_square(matrix):
            return False
                
        identity = np.identity(matrix.shape[0])
        # TODO: Add the conjugate part when we upgrade to complex numbers
        conj_transpose = matrix.transpose()

        return np.allclose(matrix @ conj_transpose, identity)
    

def hgate(vector: np.ndarray) -> np.ndarray:
    return H_GATE @ vector

def xgate(vector: np.ndarray) -> np.ndarray:
    return X_GATE @ vector
