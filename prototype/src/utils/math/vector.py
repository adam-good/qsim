import math
from typing import Tuple, Iterator
from dataclasses import dataclass
import utils.math.scalar as scalar


@dataclass(frozen=True)
class Vector:
    raw_data: Tuple[scalar.Scalar, ...]

    @property
    def shape(self) -> int:
        return len(self.raw_data)

    def __add__(self, other: Vector) -> Vector:
        if not isinstance(other, Vector):
            return NotImplemented
        return Vector(tuple(a + b for a, b in zip(self.raw_data, other.raw_data)))

    def __sub__(self, other: Vector) -> Vector:
        if not isinstance(other, Vector):
            return NotImplemented
        return Vector(tuple(a - b for a, b in zip(self.raw_data, other.raw_data)))

    def __mul__(self, other: scalar.Scalar) -> Vector:
        if not isinstance(other, scalar.Scalar):
            return NotImplemented
        return Vector(tuple(x * other for x in self.raw_data))

    def __rmul__(self, other: scalar.Scalar) -> Vector:
        return self.__mul__(other)

    def __truediv__(self, other: scalar.Scalar) -> Vector:
        if not isinstance(other, scalar.Scalar):
            return NotImplemented
        return Vector(tuple(x / other for x in self.raw_data))

    def __len__(self) -> int:
        return len(self.raw_data)

    def __getitem__(self, i: int) -> scalar.Scalar:
        return self.raw_data[i]

    def __iter__(self) -> Iterator[scalar.Scalar]:
        return iter(self.raw_data)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Vector):
            return NotImplemented
        if len(self) != len(other):
            return False
        return all(math.isclose(a, b) for a, b in zip(self, other))

    def __repr__(self):
        return f"{self.raw_data}"


def dotprod(w: Vector, v: Vector) -> scalar.Scalar:
    return sum(a * b for a, b in zip(w, v))
