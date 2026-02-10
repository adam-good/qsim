from utils.gates import hgate, xgate
import dataclasses
import numpy as np
from utils.math import vec2d_to_angle

type q_vector = np.typing.NDArray[np.float64]

def _ket0_state_factory() -> q_vector:
    return np.array([1.0, 0.0])

@dataclasses.dataclass(frozen=True)
class QuantumState:
    state_vec: q_vector = dataclasses.field(default_factory=_ket0_state_factory)

    def __post__init__(self):
        # TODO: Implement Proper Errors
        if not self.is_valid():
            raise Exception("Invalid Quantum State")

    def is_valid(self) -> bool:
        if self._x ** 2 + self._y ** 2 == 1.0:
            return True
        else:
            return False

    @property
    def to_vector(self) -> q_vector:
        return self.state_vec

    @property
    def _x(self) -> np.float64:
        return self.state_vec[0]

    @property
    def _y(self) -> np.float64:
        return self.state_vec[1]

    @property
    def angle(self) -> np.float64:
        angle = vec2d_to_angle(self._x, self._y)
        return np.float64(angle)

    @property
    def bloch_angles(self) -> np.float64:
        angle = vec2d_to_angle(self._x, self._y, lambda x: 2 * x)
        return np.float64(angle)

    @property
    def probability_distribution(self) -> q_vector:
        probabilities: q_vector = np.abs(self.state_vec) ** 2
        return probabilities


class Qubit:
    def __init__(self, state: QuantumState = QuantumState()):
        self.state = state

    def _collapse(self):
        probabilities: q_vector = self.state.probability_distribution
        outcome_idx = np.random.choice([0,1], p=probabilities)
        new_state = np.zeros(shape=(2,))
        new_state[outcome_idx] = 1.0
        self.state = QuantumState(new_state)

    def measure(self) -> QuantumState:
        # Collapse the wavefunction and return a classical bit
        self._collapse()
        return self.state

    def hadamard(self) -> Qubit:
        vector = self.state.to_vector
        state_vec = hgate(vector)
        new_state = QuantumState(state_vec)
        self.state = new_state
        return self

    def negate(self) -> Qubit:
        vector = self.state.to_vector
        state_vec: q_vector = xgate(vector)
        new_state = QuantumState(state_vec)
        self.state = new_state
        return self
        
