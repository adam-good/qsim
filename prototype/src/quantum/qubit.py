import numpy as np
from quantum.state import QuantumState, KET_0
from utils.gates import hgate, xgate
from utils.typing import q_vector

class Qubit:
    def __init__(self,
                 state: QuantumState | list[float] | np.typing.NDArray[np.float64] = QuantumState(),
                 label: str | None = "\u03C8",
                 log: bool = False):
        self.label = f"\u007C{label}\u27E9"
        self.log = log
        self.history: list[QuantumState] = [] if log else None

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
            self.history.append(self.state)

    def _update(self):
        self._log()

    def reset(self) -> Qubit:
        self.state = KET_0
        self._update()
        return self

    def measure(self) -> QuantumState:
        # Collapse the wavefunction and return a classical bit
        self._collapse()
        self._update()
        return self.state

    def hadamard(self) -> Qubit:
        vector = self.state.vector
        state_vec = hgate(vector)
        new_state = QuantumState(state_vec)
        self.state = new_state
        self._update()
        return self

    def negate(self) -> Qubit:
        vector = self.state.vector
        state_vec: q_vector = xgate(vector)
        new_state = QuantumState(state_vec)
        self.state = new_state
        self._update()
        return self

    def _to_csv_form(self) -> str:
        return f"{self.label}, {self.state.vector[0]}, {self.state.vector[1]}\n"

    def __eq__(self, other) -> bool:
        return self.state == other.state

    def __repr__(self) -> str:
        return f"{self.label} QBit({self.state.vector})"
