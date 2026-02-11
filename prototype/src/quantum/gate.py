from quantum.qubit import Qubit, QuantumState
from utils.gates import H_GATE, X_GATE
import numpy as np
import numpy.typing as npt

class Gate:
    def __init__(self, matrix: npt.NDArray[np.float64]):
        self.matrix = matrix
        
    def __call__(self, qubit: Qubit) -> np.ndarray:
        new_state = self.matrix @ qubit.state.vector
        qubit.state = QuantumState(new_state)
        return new_state

class HGate(Gate):
    def __init__(self):
        super().__init__(H_GATE)
         

class XGate(Gate):
    def __init__(self):
        super().__init__(X_GATE)
