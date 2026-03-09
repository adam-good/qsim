from typing import Annotated, Literal, TypeAlias
import numpy as np
import numpy.typing as npt

Scalar: TypeAlias = npt.DTypeLike[np.float64]
Vector: TypeAlias = Annotated[npt.NDArray[Scalar], Literal[2]]
matrix: TypeAlias = Annotated[npt.NDArray[Scalar], Literal['M', 'N']]

def to_vector(x: npt.ArrayLike) -> Vector:
    arr = np.asarray(x, dtype=Scalar)
    if arr.ndim != 1:
        raise Exception("Incorrect Array Shape for Vector")
    return arr

def to_matrix(x: npt.ArrayLike) -> matrix:
    arr = np.asarray(x, dtype=Scalar)
    if arr.ndim != 2:
        raise Exception("Incorrect Array Shape for Matrix")
    return arr
