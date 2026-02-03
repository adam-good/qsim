import numpy as np
from utils.math import vec2d_to_angle

class QuantumState:
    def __init__(self, state=np.array([1.0, 0.0])):
        self.state = state

    def to_vector(self):
        return self.state

    def x(self):
        return self.state[0]

    def y(self):
        return self.state[1]

    def to_angles(self):
        return vec2d_to_angle(self.x(), self.y())

    def to_bloch_angles(self):
        return vec2d_to_angle(self.x(), self.y(), lambda x: 2*x)

    def to_probability_distribution(self):
        probabilities = np.abs(self.state) ** 2
        return probabilities


class Qubit:
    def __init__(self, state=QuantumState()):
        self.state = state

    def measure(self):
        # Collapse the wavefunction and return a classical bit
        probabilities = np.abs(self.state.to_vector()) ** 2
        outcome = np.random.choice([0, 1], p=probabilities)
        self.state = QuantumState(np.array([int(outcome == 0), int(outcome == 1)]))
        return outcome
