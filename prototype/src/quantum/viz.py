from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import matplotlib.animation as anim
import numpy as np

from quantum.state import QuantumState

class VizQubit():
    def __init__(self, label: str, initial_state: QuantumState):
        self.label: str = label
        self.history: list[QuantumState] = [initial_state]
        self.current_state: QuantumState = initial_state

    def plot(self, ax: plt.Axes) -> plt.Line2D:
        x,y = self._get_coords()
        line, = ax.plot([0, x], [0, y], linestyle='dashed', label=self.label)
        return line
    
    def _get_coords(self, bloch=True) -> tuple[np.float64, np.float64]:
        if bloch:
            vec = self.current_state.bloch_vector
        else:
            vec = self.current_state.vector
        return (vec[0], vec[1])

def plot(psi: list[QuantumState] | dict[str, QuantumState], bloch=True):
    def get_coords(state: QuantumState) -> tuple[np.float64, np.float64]:
        if bloch:
            vec = state.bloch_vector
            return vec[0], vec[1]
        else:
            vec = state.vector
            return vec[0], vec[1]

    fig = plt.figure(figsize=[5,5])
    ax = _unit_circle(fig)

    if isinstance(psi, list):
        for p in psi:
            x,y = get_coords(p)
            ax.plot([0, x], [0, y], linestyle='dashed')
    elif isinstance(psi, dict):
        for label in psi.keys():
            p = psi[label]
            x,y = get_coords(p)
            ax.plot([0,x],[0,y],linestyle='dashed',label=label)
    plt.legend()
    
    plt.show()


