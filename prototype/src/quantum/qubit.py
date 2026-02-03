import numpy as np
from utils.math import vec2d_to_angle

class QuantumState:
    def __init__(self, state: np.ndarray = np.array([1.0, 0.0])):
        self._x = state[0]
        self._y = state[1]
        self.state = state

    def to_vector(self) -> np.ndarray:
        return self.state

    @property
    def angle(self) -> float:
        return vec2d_to_angle(self._x, self._y)

    @property
    def bloch_angles(self) -> float:
        return vec2d_to_angle(self._x, self._y, lambda x: 2 * x)

    @property
    def probability_distribution(self) -> np.ndarray:
        probabilities = np.abs(self.state) ** 2
        return probabilities


class Qubit:
    def __init__(self, state: QuantumState = QuantumState()):
        self.state = state

    def measure(self) -> int:
        # Collapse the wavefunction and return a classical bit
        probabilities = np.abs(self.state.to_vector()) ** 2
        outcome = np.random.choice([0, 1], p=probabilities)
        self.state = QuantumState(np.array([int(outcome == 0), int(outcome == 1)]))
        return outcome
