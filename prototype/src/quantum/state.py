import math
import random
import utils.math.scalar as scalar
import utils.math.vector as vector
import utils.math.helper_funcs as helper

QState = vector.Vector

KET0: QState = QState((1.0, 0.0))
KET1: QState = QState((0.0, 1.0))
KETPLUS: QState = QState((1.0, 1.0)) / math.sqrt(2)
KETMINUS: QState = QState((1.0, -1.0)) / math.sqrt(2)

Z_BASIS = (KET0, KET1)
X_BASIS = (KETPLUS, KETMINUS)


def _x(psi: QState) -> scalar.Scalar:
    return psi[0]


def _y(psi: QState) -> scalar.Scalar:
    return psi[1]


def is_valid(psi: QState) -> bool:
    return math.isclose(_x(psi) ** 2 + _y(psi) ** 2, 1.0)


def angle(psi: QState) -> scalar.Scalar:
    return helper.vec2d_to_angle(_x(psi), _y(psi))


def bloch_angle(psi: QState) -> scalar.Scalar:
    return helper.vec2d_to_angle(_x(psi), _y(psi), lambda x: 2 * x)


def to_bloch_vector(psi: QState) -> vector.Vector:
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
    basis: tuple[QState, QState], psi: QState, rng: random.Random = random.Random()
) -> QState:
    probabilities: vector.Vector = probability_distribution(basis, psi)
    random_idx: int = rng.choices([0, 1], weights=probabilities.raw_data, k=1)[0]
    return basis[random_idx]


def reset(_psi: QState | None = None) -> QState:
    return KET0
