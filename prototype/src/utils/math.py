from typing import Callable
import numpy as np
from utils.typing import scalar

def rad2deg(theta: scalar) -> scalar:
    return scalar(theta * 180 / np.pi)

def deg2rad(theta: scalar) -> scalar:
    return scalar(theta * np.pi / 180)

def vec2d_to_angle(x: scalar, y: scalar, transform_fn: Callable[[scalar], scalar] = lambda x: x) -> scalar:
    angle = np.atan2(y, x)
    angle = transform_fn(angle)
    angle = rad2deg(angle)
    while angle < 0 or angle > 360:
        angle = (angle + 360) % 360
    return scalar(angle)
