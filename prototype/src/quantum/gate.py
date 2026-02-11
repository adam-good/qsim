from quantum.qubit import Qubit, QuantumState
from utils.gates import H_GATE, X_GATE, is_unitary
import numpy as np
import numpy.typing as npt

class Gate:
    def __init__(self, matrix: npt.NDArray[np.float64]):
        if not is_unitary(matrix):
            raise Exception("Invalid Gate! Matrix Not Unitary")
        self.matrix = matrix          
    
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
