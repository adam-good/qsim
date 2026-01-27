import numpy as np

class QuantumState:
    def __init__(self, state=np.array([1.0, 0.0])):
        self.state = state

    def to_vector(self):
        return self.state

    def to_angles(self):
        angles = np.angle(self.state)
        return angles

    def to_probability_distribution(self):
        probabilities = np.abs(self.state) ** 2
        return probabilities
