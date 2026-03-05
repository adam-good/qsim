import numpy as np
import quantum.state as qstate
from utils.typing import vector


def collapse(psi: qstate.state) -> qstate.state:
    probabilities: vector = qstate.probability_distribution(psi)
    random_idx = np.random.choice([0,1], p=probabilities)
    result_states = [qstate.ket0, qstate.ket1]
    return result_states[random_idx]()
    
def reset(_psi: qstate.state) -> qstate.state:
    return qstate.ket0()

