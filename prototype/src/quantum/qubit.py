import numpy as np
from utils.math import vec2d_to_angle

class QuantumState:
    def __init__(self, state: np.ndarray = np.array([1.0, 0.0])):
        self.state = state

    def to_vector(self) -> np.ndarray:
        return self.state

    def x(self) -> float:
        return self.state[0]

    def y(self) -> float:
        return self.state[1]

    def to_angles(self) -> float:
        return vec2d_to_angle(self.x(), self.y())

    def to_bloch_angles(self) -> float:
        return vec2d_to_angle(self.x(), self.y(), lambda x: 2 * x)

    def to_probability_distribution(self) -> np.ndarray:
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
