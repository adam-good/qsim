import dataclasses
import numpy as np
from utils.math import vec2d_to_angle
from utils.typing import q_vector

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
    def _x(self) -> np.float64:
        return self.state_vec[0]

    @property
    def _y(self) -> np.float64:
        return self.state_vec[1]

    @property
    def vector(self) -> q_vector:
        return self.state_vec

    @property
    def bloch_vector(self) -> q_vector:
        angle = np.deg2rad(self.bloch_angle)
        return np.array([np.cos(angle), np.sin(angle)])

    @property
    def angle(self) -> np.float64:
        angle = vec2d_to_angle(self._x, self._y)
        return np.float64(angle)

    @property
    def bloch_angle(self) -> np.float64:
        angle = vec2d_to_angle(self._x, self._y, lambda x: 2 * x)
        return np.float64(angle)

    @property
    def probability_distribution(self) -> q_vector:
        probabilities: q_vector = np.abs(self.state_vec) ** 2
        return probabilities

    def __eq__(self, other) -> bool:
        return (self.vector == other.vector).all()

    def __repr__(self) -> str:
        theta_char = "\N{GREEK SMALL LETTER THETA}"
        bloch_char = "\N{GREEK SMALL LETTER BETA}"
        return (
            f"QState["
                    f"vec: {self.vector}, "
                    f"{theta_char}: {self.angle}, "
                    f"{bloch_char}: {self.bloch_angle}, "   
                    f"P: {self.probability_distribution}]"
                )



KET_0 = QuantumState(np.array([1,0]))
KET_1 = QuantumState(np.array([0,1]))
KET_PLUS = QuantumState(np.array([1,1]) / np.sqrt(2))
KET_MINUS = QuantumState(np.array([1,-1]) / np.sqrt(2))
