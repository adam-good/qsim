from typing import TypeAlias, Tuple, Callable
from dataclasses import dataclass

Scalar: TypeAlias = float

@dataclass(frozen=True)
class Vector:
    raw_data: Tuple[Scalar, ...]

    def _elementwise_op(self, other: Vector, op: Callable[[Scalar, Scalar], Scalar]) -> Vector:
        return Vector( tuple(op(x,y) for (x,y) in zip(self.raw_data, other.raw_data)) )

    def __add__(self, other: Vector) -> Vector:
        return self._elementwise_op(other, lambda x,y: x+y)

    def __sub__(self, other: Vector) -> Vector:
        return self._elementwise_op(other, lambda x,y: x-y)
    
    def __mul__(self, other: Vector) -> Vector:
        return self._elementwise_op(other, lambda x,y: x*y)
    
    def __div__(self, other: Vector) -> Vector:
        return self._elementwise_op(other, lambda x,y: x/y)

    def __pow__(self, other: Scalar) -> Vector:
        return Vector(tuple(x ** other for x in self.raw_data))

    def __getitem__(self, i: int) -> Scalar:
        return self.raw_data[i]

@dataclass(frozen=True)
class Matrix:
    raw_data: Tuple[Tuple[Scalar, ...], ...] # 2D Tuple so it's efficient

    @property
    def shape(self) -> Tuple[int,int]:
        return (len(self.raw_data), len(self.raw_data[0])) if self.raw_data else (0,0)

    def _elementwise_op(self, other: Matrix, op: Callable[[Scalar, Scalar], Scalar]) -> Matrix:
        raw_data = tuple(
            tuple(op(a,b) for (a,b) in row)
            for row in zip(self.raw_data, other.raw_data)
        )
        return Matrix(raw_data)


    def _dotprod(w: Tuple[Scalar], v: Tuple[Scalar]) -> Scalar:
        return sum(a*b for (a,b) in zip(w,v))

    def __add__(self, other: Matrix) -> Matrix:
        return self._elementwise_op(other, lambda x,y: x+y)

    
    def __sub__(self, other: Matrix) -> Matrix:
        return self._elementwise_op(other, lambda x,y: x-y)

    
    def __mul__(self, other: Matrix) -> Matrix:
        return self._elementwise_op(other, lambda x,y: x*y)

    
    def __div__(self, other: Matrix) -> Matrix:
        return self._elementwise_op(other, lambda x,y: x/y)

    def __matmul__(self, other: Matrix) -> Matrix:
        raw_data = tuple(
            tuple(Matrix._dotprod(a,b) for (a,b) in row)
            for row in zip(self.raw_data, other.raw_data)
        )
        return Matrix(raw_data)
