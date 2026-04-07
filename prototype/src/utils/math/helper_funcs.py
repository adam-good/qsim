import math
from typing import Callable
import utils.math.scalar as scalar


def rad2deg(theta: scalar.Scalar) -> scalar.Scalar:
    return theta * 180 / math.pi


def deg2rad(theta: scalar.Scalar) -> scalar.Scalar:
    return theta * math.pi / 180


def vec2d_to_angle(
    x: scalar.Scalar,
    y: scalar.Scalar,
    transform_fn: Callable[[scalar.Scalar], scalar.Scalar] = lambda x: x,
) -> scalar.Scalar:
    angle = math.atan2(y, x)
    angle = transform_fn(angle)
    angle = rad2deg(angle)
    while angle < 0 or angle > 360:
        angle = (angle + 360) % 360
    return angle
