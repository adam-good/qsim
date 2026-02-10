from quantum.qubit import Qubit, QuantumState
from utils.gates import hgate, xgate
import numpy as np


class Gate:
    def __call__(self, qubit: Qubit) -> np.ndarray:
        raise NotImplementedError("Subclasses must implement this method")

class HGate(Gate):
    def __call__(self, qubit: Qubit) -> np.ndarray:
        new_state = hgate(qubit.state.vector)
        qubit.state = QuantumState(new_state)
        return new_state

class XGate(Gate):
    def __call__(self, qubit: Qubit) -> np.ndarray:
        new_state = xgate(qubit.state.vector)
        qubit.state = QuantumState(new_state)
        return new_state
