import numpy as np
from typing import Callable, overload
from utils.typing import scalar, vector

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

class Matrix:
    def __init__(self, vals: list[scalar] | vector):
        if not isinstance(vals, vector):
            vals = np.array(vals)
        self._arr: vector = vals

    def _is_square(self) -> bool:
        return len(self._arr.shape) == 2 and self._arr.shape[0] == self._arr.shape[1]
    

    def _mat_mat_mul(self, other: Matrix) -> Matrix:
        return Matrix(self._arr @ other._arr)

    def _mat_vec_mul(self, other: vector) -> vector:
        return self._arr @ other
    
    def __add__(self, other: Matrix) -> Matrix:
        return Matrix(self._arr + other._arr)

    def __sub__(self, other: Matrix) -> Matrix:
        return Matrix(self._arr - other._arr)

    def __mul__(self, other: Matrix) -> Matrix:
        return Matrix(self._arr * other._arr)

    def __div__(self, other: Matrix) -> Matrix:
        return Matrix(self._arr / other._arr)

    @overload
    def __matmul__(self, other: Matrix) -> Matrix:
        ...
    @overload
    def __matmul__(self, other: vector) -> vector:
        ...
    def __matmul__(self, other):
        if isinstance(other, vector):
            return self._mat_vec_mul(other)
        elif isinstance(other, Matrix):
            return self._mat_mat_mul(other)
        else:
            raise Exception("Undefined Other Type for Matrix Matmul")


