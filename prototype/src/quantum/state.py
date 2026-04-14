import typing
import dataclasses
import math
import random
import utils.math.scalar as scalar
import utils.math.vector as vector
import utils.math.helper_funcs as helper


@dataclasses.dataclass(frozen=True)
class QState:
    vector: vector.Vector

    def __post_init__(self):
        if not vector.validate_born_rule(self.vector):
            raise ValueError("Quantum State Breaks Born's Rule")

    def __getitem__(self, i: int) -> scalar.Scalar:
        return self.vector.__getitem__(i)

    def __repr__(self):
        return f"\u007C{self.vector}\u27E9"


QBasis = typing.NewType("QBasis", tuple[QState, QState])

HADAMARD_CONST: scalar.Scalar = 1.0 / math.sqrt(2)
KET0: QState = QState(vector.Vector((1.0, 0.0)))
KET1: QState = QState(vector.Vector((0.0, 1.0)))
KETPLUS: QState = QState(vector.Vector((1, 1)) * HADAMARD_CONST)
KETMINUS: QState = QState(vector.Vector((1, -1)) * HADAMARD_CONST)
Z_BASIS: QBasis = QBasis((KET0, KET1))
X_BASIS: QBasis = QBasis((KETPLUS, KETMINUS))


def x(psi: QState) -> scalar.Scalar:
    return psi[0]


def y(psi: QState) -> scalar.Scalar:
    return psi[1]


def as_tuple(psi: QState) -> tuple[scalar.Scalar, scalar.Scalar]:
    return (x(psi), y(psi))


def is_valid(psi: QState) -> bool:
    return vector.validate_born_rule(psi.vector)

def angle(psi: QState) -> scalar.Scalar:
    return helper.vec2d_to_angle(x(psi), y(psi))


def bloch_angle(psi: QState) -> scalar.Scalar:
    return helper.vec2d_to_angle(x(psi), y(psi), lambda x: 2 * x)


def bloch_vector(psi: QState) -> vector.Vector:
    angle = helper.deg2rad(bloch_angle(psi))
    return vector.Vector((math.cos(angle), math.sin(angle)))


def amplitude(measurement: QState, state: QState) -> scalar.Scalar:
    return vector.dotprod(measurement.vector, state.vector)


def probability(measurement: QState, state: QState) -> scalar.Scalar:
    return amplitude(measurement, state) ** 2


# NOTE: This can be made more efficient later
def probability_distribution(basis: QBasis, state: QState) -> vector.Vector:
    probs = tuple(probability(m, state) for m in basis)
    return vector.Vector(probs)


def collapse(basis: QBasis, psi: QState, rng: random.Random | None = None) -> QState:
    if rng is None:
        rng = random.Random()
    probabilities: vector.Vector = probability_distribution(basis, psi)
    random_idx: int = rng.choices([0, 1], weights=probabilities.raw_data, k=1)[0]
    return basis[random_idx]


def reset(_psi: QState | None = None) -> QState:
    return KET0
