import math
from typing import Tuple, Callable, Iterator, overload
from dataclasses import dataclass
from utils.math.scalar import Scalar

@dataclass(frozen=True)
class Vector:
    raw_data: Tuple[Scalar, ...]


    def _elementwise_op(self, other: Vector, op: Callable[[Scalar, Scalar], Scalar]) -> Vector:
        return Vector( tuple(op(x,y) for (x,y) in zip(self.raw_data, other.raw_data)) )

    def _elementwise_scalar_op(self, other: Scalar, op: Callable[[Scalar, Scalar], Scalar]) -> Vector:
        return Vector( tuple(op(x, other) for x in self.raw_data))

    def _scalar_add(self, other: Scalar) -> Vector:
        return self._elementwise_scalar_op(other, lambda x,y: x+y)
    def _vector_add(self, other: Vector) -> Vector:
        return self._elementwise_op(other, lambda x,y: x+y)
    def _scalar_sub(self, other: Scalar) -> Vector:
        return self._elementwise_scalar_op(other, lambda x,y: x-y)
    def _vector_sub(self, other: Vector) -> Vector:
        return self._elementwise_op(other, lambda x,y: x-y)
    def _scalar_mul(self, other: Scalar) -> Vector:
        return self._elementwise_scalar_op(other, lambda x,y: x*y)
    def _vector_mul(self, other: Vector) -> Vector:
        return self._elementwise_op(other, lambda x,y: x*y)
    def _scalar_div(self, other: Scalar) -> Vector:
        return self._elementwise_scalar_op(other, lambda x,y: x/y)
    def _vector_div(self, other: Vector) -> Vector:
        return self._elementwise_op(other, lambda x,y: x/y)

    ###
    # Function Overloads
    ###
    @overload
    def __add__(self, other: Scalar) -> Vector: ...
    @overload
    def __add__(self, other: Vector) -> Vector: ...
    @overload
    def __sub__(self, other: Scalar) -> Vector: ...
    @overload
    def __sub__(self, other: Vector) -> Vector: ...
    @overload
    def __mul__(self, other: Scalar) -> Vector: ...
    @overload
    def __mul__(self, other: Vector) -> Vector: ...
    @overload
    def __truediv__(self, other: Scalar) -> Vector: ...
    @overload
    def __truediv__(self, other: Vector) -> Vector: ...


    ###
    # Concrete Definitions
    ###
    def __add__(self, other: Scalar | Vector) -> Vector:
        if isinstance(other, Scalar):
            return self._scalar_add(other)
        elif isinstance(other, Vector):
            return self._vector_add(other)
        else:
            raise NotImplementedError()

    def __sub__(self, other: Vector) -> Vector:
        if isinstance(other, Scalar):
            return self._scalar_sub(other)
        elif isinstance(other, Vector):
            return self._vector_sub(other)
        else:
            raise NotImplementedError()
    
    def __mul__(self, other: Vector) -> Vector:
        if isinstance(other, Scalar):
            return self._scalar_mul(other)
        elif isinstance(other, Vector):
            return self._vector_mul(other)
        else:
            raise NotImplementedError()
    
    def __truediv__(self, other: Vector) -> Vector:
        if isinstance(other, Scalar):
            return self._scalar_div(other)
        elif isinstance(other, Vector):
            return self._vector_div(other)
        else:
            raise NotImplementedError()

    def __pow__(self, other: Scalar) -> Vector:
        return Vector(tuple(x ** other for x in self.raw_data))

    def __len__(self) -> int:
        return len(self.raw_data)

    def __getitem__(self, i: int) -> Scalar:
        return self.raw_data[i]

    def __iter__(self) -> Iterator[Scalar]:
        return self.raw_data.__iter__()

    def dotprod(w: Vector, v: Vector) -> Scalar:
        return sum(a*b for (a,b) in zip(w, v))

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Vector):
            for (a,b) in zip(self, other):
                if not math.isclose(a,b):
                    return False
            return True
        else:
            raise NotImplementedError()

    def __repr__(self):
        return f"{self.raw_data}"
