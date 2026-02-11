import matplotlib.pyplot as plt
import quantum.qubit as q

def plot(psi: list[q.Qubit] | dict[str, q.Qubit]):
    fig = plt.figure(figsize=[5,5])
    ax = fig.add_subplot(1,1,1)
    ax.set_xlim(-1.2, 1.2)
    ax.set_ylim(-1.2, 1.2)
    unit_circle = plt.Circle((0,0), radius=1, edgecolor='b', facecolor='None')
    ax.add_patch(unit_circle)
#    ax.hlines(xmin=-1, xmax=1, y=0, color='red')
#    ax.vlines(ymin=-1, ymax=1, x=0, color='red')

    if isinstance(psi, list):
        for p in psi:
            ax.plot([0, p.state._x], [0, p.state._y], linestyle='dashed')
    elif isinstance(psi, dict):
        for label in psi.keys():
            p = psi[label]
            ax.plot([0,p.state._x],[0,p.state._y],linestyle='dashed',label=label)
    plt.legend()
    
    plt.show() 

