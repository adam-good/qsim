from typing import Annotated, Literal, TypeAlias, Any
import numpy as np
import numpy.typing as npt

Scalar: TypeAlias = np.floating[Any]
Vector: TypeAlias = Annotated[npt.NDArray[Scalar], Literal[2]]
Matrix: TypeAlias = Annotated[npt.NDArray[Scalar], Literal['M', 'N']]

def to_scalar(x: int | float | np.floating[Any]) -> Scalar:
    return np.float64(x)

def to_vector(x: npt.ArrayLike) -> Vector:
    arr = np.asarray(x, dtype=Scalar)
    if arr.ndim != 1:
        raise Exception("Incorrect Array Shape for Vector")
    return arr

def to_matrix(x: npt.ArrayLike) -> Matrix:
    arr = np.asarray(x, dtype=Scalar)
    if arr.ndim != 2:
        raise Exception("Incorrect Array Shape for Matrix")
    return arr
