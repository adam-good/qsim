import numpy as np
from utils.math.scalar import Scalar
from utils.math.vector import Vector
from utils.math.helper_funcs import vec2d_to_angle, deg2rad
from enum import Enum

QState = Vector

class Basis(Enum):
    KET0 = 0
    KET1 = 1
    KETPLUS = 2
    KETMINUS = 3

BASE_STATES: dict[Basis, QState] = {
    Basis.KET0 : QState((1.,0.)),
    Basis.KET1 : QState((0., 1.)),
    Basis.KETPLUS: QState((1.,1.)) / np.sqrt(2),
    Basis.KETMINUS: QState((1.,-1.)) / np.sqrt(2)
}

KET0: QState = BASE_STATES[Basis.KET0]
KET1: QState = BASE_STATES[Basis.KET1]
KETPLUS: QState = BASE_STATES[Basis.KETPLUS]
KETMINUS: QState = BASE_STATES[Basis.KETMINUS]

def _x(psi: QState) -> Scalar:
    return psi[0]

def _y(psi: QState) -> Scalar:
    return psi[1]

def is_valid(psi: QState) -> bool:
    return _x(psi)**2 + _y(psi)**2 == 1.0

def angle(psi: QState) -> Scalar:
    return vec2d_to_angle(_x(psi), _y(psi))

def bloch_angle(psi: QState) -> Scalar:
    return vec2d_to_angle(_x(psi), _y(psi),
                          lambda x: 2 * x)

# NOTE: This might not be necessary anymore
# Kinda redundant and all
def to_vector(psi: QState) -> Vector:
    return psi

def to_bloch_vector(psi: QState) -> Vector:
    angle = deg2rad(bloch_angle(psi))
    return Vector((np.cos(angle), np.sin(angle)))

def probability_distribution(psi: QState) -> Vector:
    return psi ** 2

def collapse(psi: QState) -> QState:
    probabilities: Vector = probability_distribution(psi)
    random_idx = np.random.choice([0,1], p=probabilities.raw_data)
    result_states = [KET0, KET1]
    return result_states[random_idx]

def reset(_psi: QState | None = None) -> QState:
    return KET0
