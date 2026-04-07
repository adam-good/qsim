import math
import random
from utils.math.scalar import Scalar
from utils.math.vector import Vector, dotprod
from utils.math.helper_funcs import vec2d_to_angle, deg2rad

QState = Vector

KET0: QState =  QState((1.,0.))
KET1: QState = QState((0.,1.))
KETPLUS: QState = QState((1.,1.)) / math.sqrt(2)
KETMINUS: QState = QState((1.,-1.)) / math.sqrt(2)

Z_BASIS = (KET0, KET1)
X_BASIS = (KETPLUS, KETMINUS)

def _x(psi: QState) -> Scalar:
    return psi[0]

def _y(psi: QState) -> Scalar:
    return psi[1]

def is_valid(psi: QState) -> bool:
    return math.isclose(_x(psi)**2 + _y(psi)**2, 1.0)

def angle(psi: QState) -> Scalar:
    return vec2d_to_angle(_x(psi), _y(psi))

def bloch_angle(psi: QState) -> Scalar:
    return vec2d_to_angle(_x(psi), _y(psi),
                          lambda x: 2 * x)

def to_bloch_vector(psi: QState) -> Vector:
    angle = deg2rad(bloch_angle(psi))
    return Vector((math.cos(angle), math.sin(angle)))

def amplitude(measurement: QState, state: QState) -> Scalar:
    return dotprod(measurement, state)

def probability(measurement: QState, state: QState) -> Scalar:
    return amplitude(measurement, state) ** 2

# NOTE: This can be made more efficient later
def probability_distribution(basis: tuple[QState, QState], state: QState) -> Vector:
    probs = tuple(probability(m, state) for m in basis)
    return Vector(probs)
    
def collapse(basis: tuple[QState, QState], psi: QState, rng: random.Random = random.Random()) -> QState:
    probabilities: Vector = probability_distribution(basis, psi)
    random_idx: int = rng.choices([0,1], weights=probabilities.raw_data, k=1)[0]
    return basis[random_idx]

def reset(_psi: QState | None = None) -> QState:
    return KET0
