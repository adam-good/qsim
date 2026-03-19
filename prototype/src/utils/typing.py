import math
from typing import TypeAlias, Tuple, Callable, Iterator, overload
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
    
    def __truediv__(self, other: Vector) -> Vector:
        return self._elementwise_op(other, lambda x,y: x/y)

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

@dataclass(frozen=True)
class Matrix:
    raw_data: Tuple[Tuple[Scalar, ...], ...] # 2D Tuple so it's efficient

    @property
    def shape(self) -> Tuple[int,int]:
        return (len(self.raw_data), len(self.raw_data[0])) if self.raw_data else (0,0)

    @property
    def col_vectors(self) -> Tuple[Vector, ...]:
        transpose  = tuple(zip(*self.raw_data))
        return tuple(Vector(c) for c in transpose)

    @property
    def row_vectors(self) -> Tuple[Vector, ...]:
        return tuple(Vector(c) for c in self.raw_data)

    @property
    def transpose(self) -> Matrix:
        return Matrix(tuple(zip(*self.raw_data)))

    def identity(size: int) -> Matrix:
        return Matrix(tuple(
            tuple(1 if i==j else 0 for i in range(size))
            for j in range(size))
        )
    
    def _flatten(self) -> Tuple[Scalar, ...]:
        return tuple(x for row in self.raw_data for x in row)

    ###
    # Private Math Functions
    ###
        
    def _elementwise_op(matrix_a: Matrix, matrix_b: Matrix, op: Callable[[Scalar, Scalar], Scalar]) -> Matrix:
        return Matrix(tuple(
            tuple(op(a,b) for (a,b) in zip(row_a, row_b))
            for row_a,row_b in zip(matrix_a.raw_data, matrix_b.raw_data)
        ))

    def _elementwise_scalar_op(matrix: Matrix, scalar: Scalar, op: Callable[[Scalar, Scalar], Scalar]) -> Matrix:
        return Matrix(tuple(
            tuple(op(a, scalar) for a in row)
            for row in matrix.raw_data
        ))

    def _scalar_add(matrix: Matrix, scalar: Scalar) -> Matrix:
        return Matrix._elementwise_scalar_op(matrix, scalar, lambda a,b: a+b)

    def _scalar_sub(matrix: Matrix, scalar: Scalar) -> Matrix:
        return Matrix._elementwise_scalar_op(matrix, scalar, lambda a,b: a-b)

    def _scalar_mul(matrix: Matrix, scalar: Scalar) -> Matrix:
        return Matrix._elementwise_scalar_op(matrix, scalar, lambda a,b: a*b)

    def _scalar_div(matrix: Matrix, scalar: Scalar) -> Matrix:
        return Matrix._elementwise_scalar_op(matrix, scalar, lambda a,b: a/b)

    def _matrix_add(matrix_a: Matrix, matrix_b: Matrix) -> Matrix:
        return Matrix._elementwise_op(matrix_a, matrix_b, lambda a,b: a+b)

    def _matrix_sub(matrix_a: Matrix, matrix_b: Matrix) -> Matrix:
        return Matrix._elementwise_op(matrix_a, matrix_b, lambda a,b: a-b)

    def _matrix_mul(self, matrix: Matrix) -> Matrix:
        return self._elementwise_op(matrix, lambda a,b: a*b)

    def _matrix_div(matrix_a: Matrix, matrix_b: Matrix) -> Matrix:
        return Matrix._elementwise_op(matrix_a, matrix_b, lambda a,b: a/b)

    def _vector_matmul(matrix: Matrix, vector: Vector) -> Vector:
        rows, cols = matrix.shape
        if rows != len(vector):
            raise Exception("MatVecMul incompatiable sizes")
        return Vector(tuple(
            Vector.dotprod(row, vector) for row in matrix.row_vectors
        ))

    def _matrix_matmul(a: Matrix, b: Matrix) -> Matrix:
        a_rows, a_cols = a.shape
        b_rows, b_cols = b.shape
        if a_cols != b_rows:
            raise Exception("Matrix Matmul Incomatible Matrix Shapes")
        return Matrix(tuple(
            tuple(Vector.dotprod(w,v) for v in b.col_vectors) for w in a.row_vectors
        ))

    ###
    # Math Overloads
    ###
    @overload
    def __add__(self, other: Scalar) -> Matrix: ...
    @overload
    def __add__(self, other: Matrix) -> Matrix: ...
    @overload
    def __sub__(self, other: Scalar) -> Matrix: ...
    @overload
    def __sub__(self, other: Matrix) -> Matrix: ...
    @overload
    def __mul__(self, other: Scalar) -> Matrix: ...
    @overload
    def __mul__(self, other: Matrix) -> Matrix: ...
    @overload
    def __truediv__(self, other: Scalar) -> Matrix: ...
    @overload
    def __truediv__(self, other: Matrix) -> Matrix: ...
    @overload
    def __matmul__(self, other: Vector) -> Vector: ...
    @overload
    def __matmul__(self, other: Matrix) -> Matrix: ...

    ###
    # Concrete Operator Overload Implemetations
    ###
    def __add__(self, other: Matrix | Scalar) -> Matrix:
        if isinstance(other, Matrix):
            return Matrix._matrix_add(self, other)
        elif isinstance(other, Scalar):
            return Matrix._scalar_add(self, other)
        else:
            raise NotImplementedError()

    def __sub__(self, other: Matrix | Scalar) -> Matrix:
        if isinstance(other, Matrix):
            return Matrix._matrix_sub(self, other)
        elif isinstance(other, Scalar):
            return Matrix._scalar_sub(self, other)
        else:
            raise NotImplementedError()
    
    def __mul__(self, other: Matrix) -> Matrix:
        if isinstance(other, Matrix):
            return Matrix._matrix_mul(self, other)
        elif isinstance(other, Scalar):
            return Matrix._scalar_mul(self, other)
        else:
            raise NotImplementedError()

    
    def __truediv__(self, other: Matrix) -> Matrix:
        if isinstance(other, Matrix):
            return Matrix._matrix_div(self, other)
        elif isinstance(other, Scalar):
            return Matrix._scalar_div(self, other)
        else:
            raise NotImplementedError()

    def __matmul__(self, other: Matrix | Vector) -> Matrix | Vector:
        if isinstance(other, Matrix):
            return Matrix._matrix_matmul(self, other)
        elif isinstance(other, Vector):
            return Matrix._vector_matmul(self, other)
        else:
            raise NotImplementedError("Not Implemented For Type")

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Matrix):
            for (a,b) in zip(self._flatten(), other._flatten()):
                if not math.isclose(a,b):
                    return False
            return True
        else:
            raise NotImplementedError()
        
        
