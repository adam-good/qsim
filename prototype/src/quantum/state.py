import numpy as np
import utils.typing as types
from utils.math import vec2d_to_angle, deg2rad
from enum import Enum

type QState = types.Vector

class Basis(Enum):
    KET0 = 0
    KET1 = 1
    KETPLUS = 2
    KETMINUS = 3

BASE_STATES: dict[Basis, QState] = {
    Basis.KET0:np.array([1.,0.]),
    Basis.KET1:np.array([0.,1.]),
    Basis.KETPLUS:np.array([1.,1.]) / np.sqrt(2),
    Basis.KETMINUS:np.array([1.,-1.]) / np.sqrt(2)
}

KET0: QState = BASE_STATES[Basis.KET0]
KET1: QState = BASE_STATES[Basis.KET1]
KETPLUS: QState = BASE_STATES[Basis.KETPLUS]
KETMINUS: QState = BASE_STATES[Basis.KETMINUS]

def _x(psi: QState) -> types.Scalar:
    return psi[0]

def _y(psi: QState) -> types.Scalar:
    return psi[1]

def is_valid(psi: QState) -> bool:
    return _x(psi)**2 + _y(psi)**2 == 1.0

def angle(psi: QState) -> types.Scalar:
    return vec2d_to_angle(_x(psi), _y(psi))

def bloch_angle(psi: QState) -> types.Scalar:
    return vec2d_to_angle(_x(psi), _y(psi),
                          lambda x: 2 * x)

# NOTE: This might not be necessary anymore
# Kinda redundant and all
def to_vector(psi: QState) -> types.Vector:
    return psi

def to_bloch_vector(psi: QState) -> types.Vector:
    angle = deg2rad(bloch_angle(psi))
    return types.to_vector([np.cos(angle), np.sin(angle)])

def probability_distribution(psi: QState) -> types.Vector:
    return np.abs(psi) ** 2

def collapse(psi: QState) -> QState:
    probabilities: types.Vector = probability_distribution(psi)
    random_idx = np.random.choice([0,1], p=probabilities)
    result_states = [KET0, KET1]
    return result_states[random_idx]

def reset(_psi: QState | None = None) -> QState:
    return KET0
