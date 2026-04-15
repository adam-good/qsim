import math
from typing import Tuple, overload
from dataclasses import dataclass
import utils.math.scalar as scalar
import utils.math.vector as vector


@dataclass(frozen=True)
class Matrix:
    raw_data: Tuple[Tuple[scalar.Scalar, ...], ...]

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
    @overload
    def __matmul__(self, other: Matrix) -> Matrix: ...
    @overload
    def __matmul__(self, other: vector.Vector) -> vector.Vector: ...
    def __matmul__(self, other: Matrix | vector.Vector) -> Matrix | vector.Vector:
        if isinstance(other, Matrix):
            if n_cols(self) != n_rows(other):
                raise ValueError("Matrix matmul incompatible shapes")
            return Matrix(
                tuple(
                    tuple(vector.dotprod(w, v) for v in col_vectors(other))
                    for w in row_vectors(self)
                )
            )
        elif isinstance(other, vector.Vector):
            if n_cols(self) != len(other):
                raise ValueError("Matrix-vector matmul incompatible sizes")
            return vector.Vector(
                tuple(vector.dotprod(row, other) for row in row_vectors(self))
            )
        return NotImplemented

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Matrix):
            return NotImplemented
        return all(math.isclose(a, b) for a, b in zip(flatten(self), flatten(other)))

    def __repr__(self):
        return f"{self.raw_data}"


def row_vectors(m: Matrix) -> Tuple[vector.Vector, ...]:
    return tuple(vector.Vector(r) for r in m.raw_data)


def col_vectors(m: Matrix) -> Tuple[vector.Vector, ...]:
    return tuple(
        vector.Vector(c)
        for c in zip(*m.raw_data)  # This acts as the transpose
    )


def flatten(m: Matrix) -> Tuple[scalar.Scalar, ...]:
    return tuple(x for row in m.raw_data for x in row)


def n_rows(m: Matrix) -> int:
    return len(m.raw_data) if m.raw_data else 0


def n_cols(m: Matrix) -> int:
    return len(m.raw_data[0]) if m.raw_data else 0


def shape(m: Matrix) -> Tuple[int, int]:
    return (n_rows(m), n_cols(m))


def identity(size: int) -> Matrix:
    return Matrix(
        tuple(tuple(1 if i == j else 0 for i in range(size)) for j in range(size))
    )


def transpose(m: Matrix) -> Matrix:
    return Matrix(tuple(zip(*m.raw_data)))


def is_square(m: Matrix) -> bool:
    return n_rows(m) == n_cols(m)


def is_unitary(m: Matrix) -> bool:
    if not is_square(m):
        return False
    identity_matrix = identity(n_rows(m))
    m_transpose = transpose(m)  # TODO: This needs to be the conjugate transpose
    return m @ m_transpose == identity_matrix and m_transpose @ m == identity_matrix
