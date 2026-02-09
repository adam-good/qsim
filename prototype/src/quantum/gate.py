from quantum.qubit import Qubit, QuantumState
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

class Gate:
    def __call__(self, qubit: Qubit) -> np.ndarray:
        raise NotImplementedError("Subclasses must implement this method")

class HGate(Gate):
    def __call__(self, qubit: Qubit) -> np.ndarray:
        new_state = hgate(qubit.state.to_vector())
        qubit.state = QuantumState(new_state)
        return new_state

class XGate(Gate):
    def __call__(self, qubit: Qubit) -> np.ndarray:
        new_state = xgate(qubit.state.to_vector())
        qubit.state = QuantumState(new_state)
        return new_state
