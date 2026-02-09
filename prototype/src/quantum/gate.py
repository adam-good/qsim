from quantum.qubit import Qubit, QuantumState
import numpy as np

class Gate:
    def __call__(self, qubit: Qubit) -> np.ndarray:
        raise NotImplementedError("Subclasses must implement this method")

class HGate(Gate):
    def __call__(self, qubit: Qubit) -> np.ndarray:
        h_gate = np.array([
                          [1, 1],
                          [1, -1]
                      ]) / np.sqrt(2)
        new_state = h_gate @ qubit.state.to_vector()
        qubit.state = QuantumState(new_state)
        return new_state

class XGate(Gate):
    def __call__(self, qubit: Qubit) -> np.ndarray:
        x_gate = np.array([
                          [0,1],
                          [1,0]
                      ])
        new_state = x_gate @ qubit.state.to_vector()
        qubit.state = QuantumState(new_state)
        return new_state
