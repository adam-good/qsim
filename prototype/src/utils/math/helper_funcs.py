import math
from typing import Callable
from utils.math.scalar import Scalar

def rad2deg(theta: Scalar) -> Scalar:
    return theta * 180 / math.pi

def deg2rad(theta: Scalar) -> Scalar:
    return theta * math.pi / 180

def vec2d_to_angle(x: Scalar, y: Scalar, transform_fn: Callable[[Scalar], Scalar] = lambda x: x) -> Scalar:
    angle = math.atan2(y, x)
    angle = transform_fn(angle)
    angle = rad2deg(angle)
    while angle < 0 or angle > 360:
        angle = (angle + 360) % 360
    return angle
   
