import numpy as np

def hgate(vector: np.ndarray) -> np.ndarray:
    matrix = np.array([
        [1,1],
        [1,-1]
    ]) / np.sqrt(2)
    return matrix @ vector

def xgate(vector: np.ndarray) -> np.ndarray:
    matrix = np.array([
            [0,1],
            [1,0]
        ])
    return matrix @ vector
