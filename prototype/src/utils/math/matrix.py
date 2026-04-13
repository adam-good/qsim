import math
from typing import Tuple, overload
from dataclasses import dataclass
import utils.math.scalar as scalar
import utils.math.vector as vector


@dataclass(frozen=True)
class Matrix:
    raw_data: Tuple[Tuple[scalar.Scalar, ...], ...]

    @property
    def n_rows(self) -> int:
        return len(self.raw_data) if self.raw_data else 0

    @property
    def n_cols(self) -> int:
        return len(self.raw_data[0]) if self.raw_data else 0

    @property
    def shape(self) -> Tuple[int, int]:
        return (self.n_rows, self.n_cols)

    def col_vectors(self) -> Tuple[vector.Vector, ...]:
        return tuple(
            vector.Vector(c)
            for c in zip(*self.raw_data)  # This acts as the transpose
        )

    def row_vectors(self) -> Tuple[vector.Vector, ...]:
        return tuple(vector.Vector(r) for r in self.raw_data)

    def _flatten(self) -> Tuple[scalar.Scalar, ...]:
        return tuple(x for row in self.raw_data for x in row)

    def __add__(self, other: Matrix) -> Matrix:
        if not isinstance(other, Matrix):
            return NotImplemented
        return Matrix(
            tuple(
                tuple(a + b for a, b in zip(row_a, row_b))
                for row_a, row_b in zip(self.raw_data, other.raw_data)
            )
        )

    def __sub__(self, other: Matrix) -> Matrix:
        if not isinstance(other, Matrix):
            return NotImplemented
        return Matrix(
            tuple(
                tuple(a - b for a, b in zip(row_a, row_b))
                for row_a, row_b in zip(self.raw_data, other.raw_data)
            )
        )

    def __mul__(self, other: scalar.Scalar) -> Matrix:
        if not isinstance(other, (int, float)):
            return NotImplemented
        return Matrix(tuple(tuple(a * other for a in row) for row in self.raw_data))

    def __rmul__(self, other: scalar.Scalar) -> Matrix:
        return self.__mul__(other)

    def __truediv__(self, other: scalar.Scalar) -> Matrix:
        if not isinstance(other, (int, float)):
            return NotImplemented
        return Matrix(tuple(tuple(a / other for a in row) for row in self.raw_data))

    @overload
    def __matmul__(self, other: Matrix) -> Matrix: ...
    @overload
    def __matmul__(self, other: vector.Vector) -> vector.Vector: ...
    # TODO: Clean this up
    def __matmul__(self, other: Matrix | vector.Vector) -> Matrix | vector.Vector:
        if isinstance(other, Matrix):
            if self.n_cols != other.n_rows:
                raise ValueError("Matrix matmul incompatible shapes")
            return Matrix(
                tuple(
                    tuple(vector.dotprod(w, v) for v in other.col_vectors())
                    for w in self.row_vectors()
                )
            )
        elif isinstance(other, vector.Vector):
            if self.n_cols != len(other):
                raise ValueError("Matrix-vector matmul incompatible sizes")
            return vector.Vector(
                tuple(vector.dotprod(row, other) for row in self.row_vectors())
            )
        return NotImplemented

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Matrix):
            return NotImplemented
        return all(
            math.isclose(a, b) for a, b in zip(self._flatten(), other._flatten())
        )

    def __repr__(self):
        return f"{self.raw_data}"



def identity(size: int) -> Matrix:
    return Matrix(
        tuple(tuple(1 if i == j else 0 for i in range(size)) for j in range(size))
    )

def transpose(m: Matrix) -> Matrix:
    return Matrix(tuple(zip(*m.raw_data)))

def is_square(m: Matrix) -> bool:
    return m.n_rows == m.n_cols

def is_unitary(m: Matrix) -> bool:
    if not is_square(m):
        return False
    identity_matrix = identity(m.n_rows)
    m_transpose = transpose(m)  # TODO: This needs to be the conjugate transpose
    return m @ m_transpose == identity_matrix and m_transpose @ m == identity_matrix
