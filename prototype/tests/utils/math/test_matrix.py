import unittest
from utils.math.matrix import Matrix
from utils.math.vector import Vector


class TestMatrixArithmetic(unittest.TestCase):
    def test_matrix_add(self):
        m1 = Matrix(((3, 3), (3, 3)))
        m2 = Matrix(((2, 2), (2, 2)))
        target = Matrix(((5, 5), (5, 5)))
        result = m1 + m2
        self.assertEqual(result, target)

    def test_matrix_sub(self):
        m1 = Matrix(((3, 3), (3, 3)))
        m2 = Matrix(((2, 2), (2, 2)))
        target = Matrix(((1, 1), (1, 1)))
        result = m1 - m2
        self.assertEqual(result, target)

    def test_scalar_mul(self):
        matrix = Matrix(((1, 2), (3, 4)))
        scalar = 2.0
        target = Matrix(((2, 4), (6, 8)))
        result = matrix * scalar
        self.assertEqual(result, target)

    def test_rmul(self):
        matrix = Matrix(((1, 2), (3, 4)))
        scalar = 2.0
        target = Matrix(((2, 4), (6, 8)))
        result = scalar * matrix
        self.assertEqual(result, target)

    def test_scalar_div(self):
        matrix = Matrix(((1, 2), (3, 4)))
        scalar = 2.0
        target = Matrix(((1 / 2, 2 / 2), (3 / 2, 4 / 2)))
        result = matrix / scalar
        self.assertEqual(result, target)

    def test_vector_matmul(self):
        mat = Matrix(((2, 2), (2, 2)))
        vec = Vector((3, 3))
        target = Vector((12, 12))
        result = mat @ vec
        self.assertEqual(result, target)

    def test_matrix_matmul(self):
        m1 = Matrix(((2, 2), (2, 2)))
        m2 = Matrix(((3, 3), (3, 3)))
        target = Matrix(((12, 12), (12, 12)))
        result = m1 @ m2
        self.assertEqual(result, target)

    def test_matrix_matmul_shape(self):
        m1 = Matrix(((2, 2), (2, 2)))
        m2 = Matrix(((3, 3, 3), (3, 3, 3)))
        result = m1 @ m2
        self.assertEqual(result.shape, (2, 3))

    def test_matmul_vector_shape_mismatch(self):
        mat = Matrix(((2, 2), (2, 2)))
        vec = Vector((3, 3, 3))
        with self.assertRaises(ValueError):
            mat @ vec

    def test_matmul_matrix_shape_mismatch(self):
        m1 = Matrix(((2, 2), (2, 2)))
        m2 = Matrix(((3, 3), (3, 3), (3, 3)))
        with self.assertRaises(ValueError):
            m1 @ m2

    def test_add_not_implemented(self):
        matrix = Matrix(((1, 2), (3, 4)))
        self.assertIs(
            matrix.__add__(42),  # ty: ignore[invalid-argument-type]
            NotImplemented,
        )

    def test_sub_not_implemented(self):
        matrix = Matrix(((1, 2), (3, 4)))
        self.assertIs(
            matrix.__sub__(42),  # ty: ignore[invalid-argument-type]
            NotImplemented,
        )

    def test_mul_not_implemented(self):
        matrix = Matrix(((1, 2), (3, 4)))
        self.assertIs(
            matrix.__mul__("not a scalar"),  # ty: ignore[invalid-argument-type]
            NotImplemented,
        )

    def test_truediv_not_implemented(self):
        matrix = Matrix(((1, 2), (3, 4)))
        self.assertIs(
            matrix.__truediv__("not a scalar"),  # ty: ignore[invalid-argument-type]
            NotImplemented,
        )

    def test_matmul_not_implemented(self):
        matrix = Matrix(((1, 2), (3, 4)))
        self.assertIs(
            matrix.__matmul__(42),  # ty: ignore[invalid-argument-type]
            NotImplemented,
        )


class TestMatrixProperties(unittest.TestCase):
    def test_matrix_row_vectors(self):
        matrix = Matrix(((1, 2), (3, 4)))
        target = (Vector((1, 2)), Vector((3, 4)))
        result = matrix.row_vectors()
        self.assertEqual(result, target)

    def test_matrix_col_vectors(self):
        matrix = Matrix(((1, 2), (3, 4)))
        target = (Vector((1, 3)), Vector((2, 4)))
        result = matrix.col_vectors()
        self.assertEqual(result, target)

    def test_matrix_transpose(self):
        matrix = Matrix(((1, 2, 3), (4, 5, 6)))
        target = Matrix(((1, 4), (2, 5), (3, 6)))
        result = matrix.transpose()
        self.assertEqual(result, target)

    def test_matrix_is_square(self):
        matrix = Matrix(((1, 2), (3, 4)))
        self.assertTrue(matrix.is_square())

        matrix = Matrix(((1, 2, 3), (4, 5, 6)))
        self.assertFalse(matrix.is_square())

    def test_matrix_is_unitary(self):
        matrix = Matrix(((1, 0), (0, 1)))
        self.assertTrue(matrix.is_unitary())

        matrix = Matrix(((1, 1), (1, -1)))
        self.assertFalse(matrix.is_unitary())


if __name__ == "__main__":
    unittest.main()
