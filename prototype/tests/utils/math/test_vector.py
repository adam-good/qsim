import unittest
from utils.math.vector import Vector

class TestVector(unittest.TestCase):
    def test_scalar_add(self):
        vector = Vector((1,2))
        scalar = 2.
        target = Vector((3,4))
        result = vector + scalar
        self.assertEqual(result, target)

    def test_vector_add(self):
        v1 = Vector((1,2))
        v2 = Vector((3,4))
        target = Vector((4,6))
        result = v1+v2
        self.assertEqual(result, target)

    def test_scalar_sub(self):
        vector = Vector((1,2))
        scalar = 2.
        target = Vector((-1,0))
        result = vector - scalar
        self.assertEqual(result, target)
        
    def test_vector_sub(self):
        v1 = Vector((1,2))
        v2 = Vector((3,4))
        target = Vector((-2, -2))
        result = v1-v2
        self.assertEqual(result, target)

    def test_scalar_mul(self):
        vector = Vector((1,2))
        scalar = 2.
        target = Vector((2,4))
        result = vector * scalar
        self.assertEqual(result, target)
        
    def test_vector_mul(self):
        v1 = Vector((1,2))
        v2 = Vector((3,4))
        target = Vector((3,8))
        result = v1*v2
        self.assertEqual(result, target)


    def test_scalar_div(self):
        vector = Vector((1,2))
        scalar = 2.
        target = Vector((1/2,2/2))
        result = vector / scalar
        self.assertEqual(result, target)

    def test_vector_div(self):
        v1 = Vector((1,2))
        v2 = Vector((3,4))
        target = Vector((1/3, 2/4))
        result = v1/v2
        self.assertEqual(result, target)

    def test_pow(self):
        vec = Vector((1,2))
        scalar = 3
        target = Vector((1, 8))
        result = vec ** scalar
        self.assertEqual(result, target)

    def test_dotprod(self):
        v1 = Vector((1,2))
        v2 = Vector((3,4))
        target = 11
        result = Vector.dotprod(v1,v2)
        self.assertEqual(result,target)
