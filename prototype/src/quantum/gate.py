from black.trans import is_valid_index_factory
from quantum.qubit import Qubit, QuantumState
from utils.gates import H_GATE, X_GATE
import numpy as np
import numpy.typing as npt

class Gate:
    def __init__(self, matrix: npt.NDArray[np.float64]):
        if not self._is_valid(matrix):
            raise Exception("Invalid Gate! Matrix Not Unitary")
        self.matrix = matrix

    def _is_valid(self,matrix: npt.NDArray[np.float64]) -> bool:
        def is_square(matrix: npt.NDArray) -> bool:
            return len(matrix.shape) == 2 and matrix.shape[0] == matrix.shape[1]

        if not is_square(matrix):
            return False
                
        identity = np.identity(matrix.shape[0])
        # TODO: Add the conjugate part when we upgrade to complex numbers
        conj_transpose = matrix.transpose()

        return np.allclose(matrix @ conj_transpose, identity)
    
    def __call__(self, qubit: Qubit) -> np.ndarray:
        new_state = self.matrix @ qubit.state.vector
        qubit.state = QuantumState(new_state)
        return new_state

    def __matmul__(self, other: Gate | Qubit | QuantumState) -> Gate | QuantumState:
        if isinstance(other, Gate):
            return Gate(self.matrix @ other.matrix)
        elif isinstance(other, Qubit):
            state = QuantumState(self.matrix @ other.state.vector)
            other.state = state
            return state
        elif isinstance(other, QuantumState):
            return QuantumState(self.matrix @ other.vector)
              

class HGate(Gate):
    def __init__(self):
        super().__init__(H_GATE)
         

class XGate(Gate):
    def __init__(self):
        super().__init__(X_GATE)
