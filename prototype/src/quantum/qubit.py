import dataclasses
import numpy as np
import typing
from utils.gates import hgate, xgate
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

class Qubit:
    def __init__(self,
                 id: str | None = "\u03C8",
                 state: QuantumState | list[float] | np.typing.NDArray[np.float64] = QuantumState(),
                 log: typing.IO | None = None):
        self.id = f"\u007C{id}\u27E9"
        self.log = log
        if isinstance(state, QuantumState):
            self._from_quantumstate(state)
        elif isinstance(state, list):
            self._from_list(state)
        elif isinstance(state, np.typing.NDArray[np.float64]):
            self._from_ndarr(state)

    def _from_quantumstate(self, state: QuantumState):
        self.state: QuantumState = state
    def _from_list(self, vec_list: list):
        self.state: QuantumState = QuantumState(np.array(vec_list))
    def _from_ndarr(self, vec: np.typing.NDArray[np.float64]):
        self.state: QuantumState = QuantumState(vec)

    def _collapse(self):
        probabilities: q_vector = self.state.probability_distribution
        outcome_idx = np.random.choice([0,1], p=probabilities)
        new_state = np.zeros(shape=(2,))
        new_state[outcome_idx] = 1.0
        self.state = QuantumState(new_state)

    def _log(self):
        if self.log:
            self.log.write(self._to_csv_form())

    def measure(self) -> QuantumState:
        # Collapse the wavefunction and return a classical bit
        self._collapse()
        self._log()
        return self.state

    def hadamard(self) -> Qubit:
        vector = self.state.vector
        state_vec = hgate(vector)
        new_state = QuantumState(state_vec)
        self.state = new_state
        self._log()
        return self

    def negate(self) -> Qubit:
        vector = self.state.vector
        state_vec: q_vector = xgate(vector)
        new_state = QuantumState(state_vec)
        self.state = new_state
        self._log()
        return self

    def _to_csv_form(self) -> str:
        return f"{self.id}, {self.state.vector[0]}, {self.state.vector[1]}\n"

    def __eq__(self, other) -> bool:
        return self.state == other.state

    def __repr__(self) -> str:
        return f"{self.id} QBit({self.state.vector})"
