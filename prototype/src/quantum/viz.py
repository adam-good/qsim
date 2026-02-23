from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import matplotlib.animation as anim
import quantum.qubit as q
import numpy as np

def plot(psi: list[q.QuantumState] | dict[str, q.QuantumState], bloch=True):
    def get_coords(state: q.QuantumState) -> tuple[np.float64, np.float64]:
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


def plot_quantum_state(ax: plt.Axes, state: q.QuantumState, label: str | None = None, bloch=True) -> list[plt.Line2D]:
    def get_coords(state: q.QuantumState) -> tuple[np.float64, np.float64]:
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

def _get_coords(state: q.QuantumState, bloch=True) -> tuple[np.float64, np.float64]:
    if bloch:
        vec = state.bloch_vector
    else:
        vec = state.vector
    return (vec[0], vec[1])

def animate_state_timeseries(data: list[q.QuantumState], label: str | None = None, bloch=True):
    fig = plt.figure(figsize=[5,5])
    ax = _unit_circle(fig)
    p, = ax.plot([], [], linestyle='dashed', label=label)

    def init():
        p.set_data([],[])
        return p,

    def update(i):
        circ = plt.Circle((0,0), radius=1, edgecolor='b', facecolor='None')
        ax.add_patch(circ)
        x,y = _get_coords(data[i], bloch=bloch)
        p.set_data([0,x], [0,y])

        return p,

    animation = anim.FuncAnimation(fig, update, init_func = init, frames = len(data))
    return animation
        
