import numpy as np
from utils.math import vec2d_to_angle, deg2rad
from utils.typing import vector, scalar

type qstate = vector

def ket0() -> qstate:
    return np.array([1., 0.])
def ket1() -> qstate:
    return np.array([0., 1.])
def ket_plus() -> qstate:
    return np.array([1.,1.] / np.sqrt(2))
def key_minus() -> qstate:
    return np.array([1.,-1.] / np.sqrt(2))

def _x(psi: qstate) -> scalar:
    return psi[0]

def _y(psi: qstate) -> scalar:
    return psi[1]

def is_valid(psi: qstate) -> bool:
    return _x(psi)**2 + _y(psi)**2 == 1.0

def angle(psi: qstate) -> scalar:
    return vec2d_to_angle(_x(psi), _y(psi))

def bloch_angle(psi: qstate) -> scalar:
    return vec2d_to_angle(_x(psi), _y(psi),
                          lambda x: 2 * x)

# NOTE: This might not be necessary anymore
# Kinda redundant and all
def to_vector(psi: qstate) -> vector:
    return psi

def to_bloch_vector(psi: qstate) -> vector:
    angle = deg2rad(bloch_angle(psi))
    return vector([np.cos(angle), np.sin(angle)])

def probability_distribution(psi: qstate) -> vector:
    return np.abs(psi) ** 2

