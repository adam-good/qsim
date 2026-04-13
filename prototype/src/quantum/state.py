from typing import NewType
import math
import random
import utils.math.scalar as scalar
import utils.math.vector as vector
import utils.math.helper_funcs as helper

QState = NewType("QState", vector.Vector)

def qstate_from_data(data: tuple[scalar.Scalar, scalar.Scalar]) -> QState:
    return QState(vector.Vector(data))

def qstate_from_vector(vec: vector.Vector) -> QState:
    return QState(vec)

hadamard_constant: scalar.Scalar = 1.0 / math.sqrt(2)
KET0: QState = qstate_from_data((1.0, 0.0))
KET1: QState = qstate_from_data((0.0, 1.0))
KETPLUS: QState = qstate_from_data((hadamard_constant, hadamard_constant))
KETMINUS: QState = qstate_from_data((hadamard_constant, -hadamard_constant))
Z_BASIS = (KET0, KET1)
X_BASIS = (KETPLUS, KETMINUS)


def x(psi: QState) -> scalar.Scalar:
    return psi[0]


def y(psi: QState) -> scalar.Scalar:
    return psi[1]

def as_tuple(psi: QState) -> tuple[scalar.Scalar, scalar.Scalar]:
    return (x(psi), y(psi))


def is_valid(psi: QState) -> bool:
    return math.isclose(x(psi) ** 2 + y(psi) ** 2, 1.0)


def angle(psi: QState) -> scalar.Scalar:
    return helper.vec2d_to_angle(x(psi), y(psi))


def bloch_angle(psi: QState) -> scalar.Scalar:
    return helper.vec2d_to_angle(x(psi), y(psi), lambda x: 2 * x)


def bloch_vector(psi: QState) -> vector.Vector:
    angle = helper.deg2rad(bloch_angle(psi))
    return vector.Vector((math.cos(angle), math.sin(angle)))


def amplitude(measurement: QState, state: QState) -> scalar.Scalar:
    return vector.dotprod(measurement, state)


def probability(measurement: QState, state: QState) -> scalar.Scalar:
    return amplitude(measurement, state) ** 2


# NOTE: This can be made more efficient later
def probability_distribution(
    basis: tuple[QState, QState], state: QState
) -> vector.Vector:
    probs = tuple(probability(m, state) for m in basis)
    return vector.Vector(probs)


def collapse(
    basis: tuple[QState, QState], psi: QState, rng: random.Random | None = None
) -> QState:
    if rng is None:
        rng = random.Random()
    probabilities: vector.Vector = probability_distribution(basis, psi)
    random_idx: int = rng.choices([0, 1], weights=probabilities.raw_data, k=1)[0]
    return basis[random_idx]


def reset(_psi: QState | None = None) -> QState:
    return KET0
