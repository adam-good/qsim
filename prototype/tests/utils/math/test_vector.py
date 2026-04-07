import unittest
from utils.math.vector import Vector, dotprod


class TestVector(unittest.TestCase):
    def test_vector_add(self):
        v1 = Vector((1, 2))
        v2 = Vector((3, 4))
        target = Vector((4, 6))
        result = v1 + v2
        self.assertEqual(result, target)

    def test_vector_sub(self):
        v1 = Vector((1, 2))
        v2 = Vector((3, 4))
        target = Vector((-2, -2))
        result = v1 - v2
        self.assertEqual(result, target)

    def test_scalar_mul(self):
        vector = Vector((1, 2))
        scalar = 2.0
        target = Vector((2, 4))
        result = vector * scalar
        self.assertEqual(result, target)

    def test_rmul(self):
        vector = Vector((1, 2))
        scalar = 2.0
        target = Vector((2, 4))
        result = scalar * vector
        self.assertEqual(result, target)

    def test_scalar_div(self):
        vector = Vector((1, 2))
        scalar = 2.0
        target = Vector((1 / 2, 2 / 2))
        result = vector / scalar
        self.assertEqual(result, target)

    def test_dotprod(self):
        v1 = Vector((1, 2))
        v2 = Vector((3, 4))
        target = 11
        result = dotprod(v1, v2)
        self.assertEqual(result, target)

    def test_len(self):
        vector = Vector((1, 2, 3))
        self.assertEqual(len(vector), 3)

    def test_getitem(self):
        vector = Vector((10, 20, 30))
        self.assertEqual(vector[0], 10)
        self.assertEqual(vector[2], 30)

    def test_iter(self):
        vector = Vector((1, 2, 3))
        self.assertEqual(list(vector), [1, 2, 3])

    def test_eq_not_implemented(self):
        vector = Vector((1, 2))
        self.assertIs(vector.__eq__("not a vector"), NotImplemented)

    def test_add_not_implemented(self):
        vector = Vector((1, 2))
        self.assertIs(
            vector.__add__(42),  # type: ignore[arg-tag]
            NotImplemented,
        )

    def test_sub_not_implemented(self):
        vector = Vector((1, 2))
        self.assertIs(
            vector.__sub__(42),  # type: ignore[arg-tag]
            NotImplemented,
        )

    def test_mul_not_implemented(self):
        vector = Vector((1, 2))
        self.assertIs(
            vector.__mul__("not a scalar"),  # type: ignore[arg-tag]
            NotImplemented,
        )

    def test_div_not_implemented(self):
        vector = Vector((1, 2))
        self.assertIs(
            vector.__truediv__("not a scalar"),  # type: ignore[arg-tag]
            NotImplemented,
        )

    def test_eq_different_lengths(self):
        v1 = Vector((1, 2))
        v2 = Vector((1, 2, 3))
        self.assertFalse(v1 == v2)

    def test_eq_close_values(self):
        v1 = Vector((1.0, 2.0))
        v2 = Vector((1.0 + 1e-10, 2.0 - 1e-10))
        self.assertEqual(v1, v2)


if __name__ == "__main__":
    unittest.main()
