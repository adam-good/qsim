from typing import Callable
import numpy as np

def rad2deg(theta: float) -> float:
    return theta * 180 / np.pi

def deg2rad(theta: float) -> float:
    return theta * np.pi / 180

def vec2d_to_angle(x: float, y: float, transform_fn: Callable[[float], float] = lambda x: x) -> float:
    angle = np.atan2(y, x)
    angle = transform_fn(angle)
    angle = rad2deg(angle)
    while angle < 0 or angle > 360:
        angle = (angle + 360) % 360
    return angle
