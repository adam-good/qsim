import numpy as np
from typing import Callable
from utils.typing import Scalar

def rad2deg(theta: Scalar) -> Scalar:
    return theta * 180 / np.pi

def deg2rad(theta: Scalar) -> Scalar:
    return theta * np.pi / 180

def vec2d_to_angle(x: Scalar, y: Scalar, transform_fn: Callable[[Scalar], Scalar] = lambda x: x) -> Scalar:
    angle = np.atan2(y, x)
    angle = transform_fn(angle)
    angle = rad2deg(angle)
    while angle < 0 or angle > 360:
        angle = (angle + 360) % 360
    return angle

