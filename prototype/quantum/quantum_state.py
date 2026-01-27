import numpy as np

class QuantumState:
    def __init__(self, state=np.array([1.0, 0.0])):
        self.state = state

    def measure(self):
        # Collapse the wavefunction and return a classical bit
        probabilities = np.abs(self.state) ** 2
        outcome = np.random.choice([0, 1], p=probabilities)
        self.state = np.array([int(outcome == 0), int(outcome == 1)])
        return outcome

    def to_vector(self):
        # Return the state vector as a NumPy array
        return self.state

    def to_angles(self):
        # Convert the state vector to angles (e.g., for visualization)
        angles = np.angle(self.state)
        return angles

    def to_probability_distribution(self):
        # Return the probability distribution of the state
        probabilities = np.abs(self.state) ** 2
        return probabilities
