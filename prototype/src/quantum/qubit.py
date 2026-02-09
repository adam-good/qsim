import dataclasses
import numpy as np
from utils.math import vec2d_to_angle

def _ket0_state_factory():
    return np.array([1.0, 0.0])

@dataclasses.dataclass(frozen=True)
class QuantumState:
    state: np.ndarray = dataclasses.field(default_factory=_ket0_state_factory)

    def __post__init__(self):
        # TODO: Implement Proper Errors
        if not self.is_valid():
            raise Exception("Invalid Quantum State")

    def is_valid(self) -> bool:
        if self._x ** 2 + self._y ** 2 == 1.0:
            return True
        else:
            return False

    def to_vector(self) -> np.ndarray:
        return self.state

    @property
    def _x(self) -> float:
        return self.state[0]

    @property
    def _y(self) -> float:
        return self.state[1]

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

    def _collapse(self):
        probabilities = self.state.probability_distribution
        outcome_idx = np.random.choice([0,1], p=probabilities)
        new_state = np.zeros(shape=(2,))
        new_state[outcome_idx] = 1.0
        self.state = QuantumState(new_state)

    def measure(self) -> QuantumState:
        # Collapse the wavefunction and return a classical bit
        self._collapse()
        return self.state
