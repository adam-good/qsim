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


def hgate(vector: np.ndarray) -> np.ndarray:
    return H_GATE @ vector

def xgate(vector: np.ndarray) -> np.ndarray:
    return X_GATE @ vector
