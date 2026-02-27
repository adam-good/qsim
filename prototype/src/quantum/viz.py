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


def plot_quantum_state(ax: plt.Axes, state: QuantumState, label: str | None = None, bloch=True) -> list[plt.Line2D]:
    def get_coords(state: QuantumState) -> tuple[np.float64, np.float64]:
        if bloch:
            vec = state.bloch_vector
            return vec[0], vec[1]
        else:
            vec = state.vector
            return vec[0], vec[1]
    x,y = get_coords(state)
    p = ax.plot([0,x], [0,y], linestyle='dashed', label="")
    return p

def _unit_circle(fig: Figure) -> plt.Axes:
    ax = fig.add_subplot(1,1,1)
    ax.set_xlim(-1.1, 1.1)
    ax.set_ylim(-1.1, 1.1)
    circ = plt.Circle((0,0), radius=1, edgecolor='b', facecolor='None')
    ax.add_patch(circ)

    return ax

def _get_coords(state: QuantumState, bloch=True) -> tuple[np.float64, np.float64]:
    if bloch:
        vec = state.bloch_vector
    else:
        vec = state.vector
    return (vec[0], vec[1])

def animate_state_timeseries(data: dict[str,list[QuantumState]], bloch=True):
    fig = plt.figure(figsize=[5,5])
    ax = _unit_circle(fig)
    lines = {label:ax.plot([],[], linestyle='dashed', label=label) for label in data.keys()}
    lines = {label:line for (label, (line,)) in lines.items()}
    fig.legend()

    def init():
        for key in data.keys():
            line = lines[key]
            line.set_data([],[])
        return [lines[key] for key in data.keys()]

    def update(i):
        circ = plt.Circle((0,0), radius=1, edgecolor='b', facecolor='None')
        ax.add_patch(circ)
        for (label,line) in lines.items():
            if len(data[label]) > i:
                x,y = _get_coords(data[label][i], bloch=bloch)
                line.set_data([0,x], [0,y])
            else:
                line.set_data([],[])

        return [lines[key] for key in data.keys()]

    animation = anim.FuncAnimation(fig, update, init_func = init, frames = max([len(data[label]) for label in data.keys()]))
    return animation
        
