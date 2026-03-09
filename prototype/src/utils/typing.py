from typing import Annotated, Literal, TypeAlias
import numpy as np
import numpy.typing as npt

scalar: TypeAlias = npt.DTypeLike[np.float64]
vector: TypeAlias = Annotated[npt.NDArray[scalar], Literal[2]]
matrix: TypeAlias = Annotated[npt.NDArray[scalar], Literal['M', 'N']]

def to_vector(x: npt.ArrayLike) -> vector:
    arr = np.asarray(x, dtype=scalar)
    if arr.ndim != 1:
        raise Exception("Incorrect Array Shape for Vector")
    return arr

def to_matrix(x: npt.ArrayLike) -> matrix:
    arr = np.asarray(x, dtype=scalar)
    if arr.ndim != 2:
        raise Exception("Incorrect Array Shape for Matrix")
    return arr
