import numpy as np
from utils.math import vec2d_to_angle, deg2rad
from utils.typing import vector, scalar
from enum import Enum

type state = vector

class Basis(Enum):
    KET0 = 0
    KET1 = 1
    KETPLUS = 2
    KETMINUS = 3

BASE_STATES: dict[Basis, state] = {
    Basis.KET0:np.array([1.,0.]),
    Basis.KET1:np.array([0.,1.]),
    Basis.KETPLUS:np.array([1.,1.]) / np.sqrt(2),
    Basis.KETMINUS:np.array([1.,-1.]) / np.sqrt(2)
}

KET0: state = BASE_STATES[Basis.KET0]
KET1: state = BASE_STATES[Basis.KET1]
KETPLUS: state = BASE_STATES[Basis.KETPLUS]
KETMINUS: state = BASE_STATES[Basis.KETMINUS]

def _x(psi: state) -> scalar:
    return psi[0]

def _y(psi: state) -> scalar:
    return psi[1]

def is_valid(psi: state) -> bool:
    return _x(psi)**2 + _y(psi)**2 == 1.0

def angle(psi: state) -> scalar:
    return vec2d_to_angle(_x(psi), _y(psi))

def bloch_angle(psi: state) -> scalar:
    return vec2d_to_angle(_x(psi), _y(psi),
                          lambda x: 2 * x)

# NOTE: This might not be necessary anymore
# Kinda redundant and all
def to_vector(psi: state) -> vector:
    return psi

def to_bloch_vector(psi: state) -> vector:
    angle = deg2rad(bloch_angle(psi))
    return vector([np.cos(angle), np.sin(angle)])

def probability_distribution(psi: state) -> vector:
    return np.abs(psi) ** 2

def collapse(psi: state) -> state:
    probabilities: vector = probability_distribution(psi)
    random_idx = np.random.choice([0,1], p=probabilities)
    result_states = [KET0, KET1]
    return result_states[random_idx]
