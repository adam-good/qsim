import typing
import matplotlib.pyplot as plt
import quantum.qubit as q
import numpy as np

def plot(psi: list[q.Qubit] | dict[str, q.Qubit], bloch=True):
    def get_coords(qubit: q.Qubit) -> tuple[np.float64, np.float64]:
        if bloch:
            vec = qubit.state.bloch_vector
            return vec[0], vec[1]
        else:
            vec = qubit.state.vector
            return vec[0], vec[1]
    
    fig = plt.figure(figsize=[5,5])
    ax = fig.add_subplot(1,1,1)
    ax.set_xlim(-1.2, 1.2)
    ax.set_ylim(-1.2, 1.2)
    unit_circle = plt.Circle((0,0), radius=1, edgecolor='b', facecolor='None')
    ax.add_patch(unit_circle)

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

QSIM_CSV_HEADER: str = "id,x,y\n"
def open_csv(name: str) -> typing.IO:
    f = open(name, "w")
    f.write(QSIM_CSV_HEADER)
    return f
