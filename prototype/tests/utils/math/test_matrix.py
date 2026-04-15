import unittest
import utils.math.matrix as mat
import utils.math.vector as vec


class TestMatrixArithmetic(unittest.TestCase):
    def test_matrix_add(self):
        m1 = mat.Matrix(((3, 3), (3, 3)))
        m2 = mat.Matrix(((2, 2), (2, 2)))
        target = mat.Matrix(((5, 5), (5, 5)))
        result = m1 + m2
        self.assertEqual(result, target)

    def test_matrix_sub(self):
        m1 = mat.Matrix(((3, 3), (3, 3)))
        m2 = mat.Matrix(((2, 2), (2, 2)))
        target = mat.Matrix(((1, 1), (1, 1)))
        result = m1 - m2
        self.assertEqual(result, target)

    def test_scalar_mul(self):
        matrix = mat.Matrix(((1, 2), (3, 4)))
        scalar = 2.0
        target = mat.Matrix(((2, 4), (6, 8)))
        result = matrix * scalar
        self.assertEqual(result, target)

    def test_rmul(self):
        matrix = mat.Matrix(((1, 2), (3, 4)))
        scalar = 2.0
        target = mat.Matrix(((2, 4), (6, 8)))
        result = scalar * matrix
        self.assertEqual(result, target)

    def test_scalar_div(self):
        matrix = mat.Matrix(((1, 2), (3, 4)))
        scalar = 2.0
        target = mat.Matrix(((1 / 2, 2 / 2), (3 / 2, 4 / 2)))
        result = matrix / scalar
        self.assertEqual(result, target)

    def test_vector_matmul(self):
        matrix = mat.Matrix(((2, 2), (2, 2)))
        vector = vec.Vector((3, 3))
        target = vec.Vector((12, 12))
        result = matrix @ vector
        self.assertEqual(result, target)

    def test_matrix_matmul(self):
        m1 = mat.Matrix(((2, 2), (2, 2)))
        m2 = mat.Matrix(((3, 3), (3, 3)))
        target = mat.Matrix(((12, 12), (12, 12)))
        result = m1 @ m2
        self.assertEqual(result, target)

    def test_matrix_matmul_shape(self):
        m1 = mat.Matrix(((2, 2), (2, 2)))
        m2 = mat.Matrix(((3, 3, 3), (3, 3, 3)))
        result = m1 @ m2
        self.assertEqual(mat.shape(result), (2, 3))

    def test_matmul_vector_shape_mismatch(self):
        matrix = mat.Matrix(((2, 2), (2, 2)))
        vector = vec.Vector((3, 3, 3))
        with self.assertRaises(ValueError):
            matrix @ vector

    def test_matmul_matrix_shape_mismatch(self):
        m1 = mat.Matrix(((2, 2), (2, 2)))
        m2 = mat.Matrix(((3, 3), (3, 3), (3, 3)))
        with self.assertRaises(ValueError):
            m1 @ m2

    def test_add_not_implemented(self):
        matrix = mat.Matrix(((1, 2), (3, 4)))
        self.assertIs(
            matrix.__add__(42),  # type: ignore[invalid-argument-type]
            NotImplemented,
        )

    def test_sub_not_implemented(self):
        matrix = mat.Matrix(((1, 2), (3, 4)))
        self.assertIs(
            matrix.__sub__(42),  # type: ignore[invalid-argument-type]
            NotImplemented,
        )

    def test_mul_not_implemented(self):
        matrix = mat.Matrix(((1, 2), (3, 4)))
        self.assertIs(
            matrix.__mul__("not a scalar"),  # type: ignore[invalid-argument-type]
            NotImplemented,
        )

    def test_truediv_not_implemented(self):
        matrix = mat.Matrix(((1, 2), (3, 4)))
        self.assertIs(
            matrix.__truediv__("not a scalar"),  # type: ignore[invalid-argument-type]
            NotImplemented,
        )

    def test_matmul_not_implemented(self):
        matrix = mat.Matrix(((1, 2), (3, 4)))
        self.assertIs(
            matrix.__matmul__(42),  # type: ignore[invalid-argument-type]
            NotImplemented,
        )


class TestMatrixProperties(unittest.TestCase):
    def test_matrix_row_vectors(self):
        matrix = mat.Matrix(((1, 2), (3, 4)))
        target = (vec.Vector((1, 2)), vec.Vector((3, 4)))
        result = mat.row_vectors(matrix)
        self.assertEqual(result, target)

    def test_matrix_col_vectors(self):
        matrix = mat.Matrix(((1, 2), (3, 4)))
        target = (vec.Vector((1, 3)), vec.Vector((2, 4)))
        result = mat.col_vectors(matrix)
        self.assertEqual(result, target)

    def test_matrix_transpose(self):
        matrix = mat.Matrix(((1, 2, 3), (4, 5, 6)))
        target = mat.Matrix(((1, 4), (2, 5), (3, 6)))
        result = mat.transpose(matrix)
        self.assertEqual(result, target)

    def test_matrix_is_square(self):
        matrix = mat.Matrix(((1, 2), (3, 4)))
        self.assertTrue(mat.is_square(matrix))

        matrix = mat.Matrix(((1, 2, 3), (4, 5, 6)))
        self.assertFalse(mat.is_square(matrix))

    def test_matrix_is_unitary(self):
        matrix = mat.Matrix(((1, 0), (0, 1)))
        self.assertTrue(mat.is_unitary(matrix))

        matrix = mat.Matrix(((1, 1), (1, -1)))
        self.assertFalse(mat.is_unitary(matrix))


if __name__ == "__main__":
    unittest.main()
