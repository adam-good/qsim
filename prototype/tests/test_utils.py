import utils.math as math
from utils.typing import Vector, Matrix
from math import pi
import unittest

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

class TestMatrixArithmatic(unittest.TestCase):
    def test_scalar_add(self):
        matrix = Matrix( ((1,2),(3,4)) )
        scalar = 2.
        target = Matrix( ((3,4),(5,6)) )
        result = matrix+scalar
        self.assertEqual(result, target)

    def test_scalar_sub(self):
        matrix = Matrix( ((1,2),(3,4)) )
        scalar = 2.
        target = Matrix( ((-1,0),(1,2)) )
        result = matrix - scalar
        self.assertEqual(result, target)

    def test_scalar_mul(self):
        matrix = Matrix( ((1,2),(3,4)) )
        scalar = 2.
        target = Matrix( ((2,4),(6,8)) )
        result = matrix * scalar
        self.assertEqual(result, target)

    def test_scalar_div(self):
        matrix = Matrix( ((1,2),(3,4)) )
        scalar = 2.
        target = Matrix( ((1/2,2/2),(3/2,4/2)) )
        result = matrix / scalar
        self.assertEqual(result, target)

    def test_elementwise_add(self):
        m1 = Matrix( ((3,3),(3,3)) )
        m2 = Matrix( ((2,2),(2,2)))
        target = Matrix( ((5,5),(5,5)) )
        result = m1+m2
        self.assertEqual(result, target)

    def test_elementwise_sub(self):
        m1 = Matrix( ((3,3),(3,3)) )
        m2 = Matrix( ((2,2),(2,2)) )
        target = Matrix( ((1,1),(1,1)) )
        result = m1 - m2
        self.assertEqual(result, target)

    def test_elementwise_mul(self):
        m1 = Matrix( ((3,3),(3,3)) )
        m2 = Matrix( ((2,2),(2,2)) )
        target = Matrix( ((6,6),(6,6)) )
        result = m1 * m2
        self.assertEqual(result, target)

    def test_elementwise_div(self):
        m1 = Matrix( ((3,3),(3,3)) )
        m2 = Matrix( ((2,2),(2,2)) )
        target = Matrix( ((3/2,3/2),(3/2,3/2)) )
        result = m1 / m2
        self.assertEqual(result, target)

    def test_vector_matmul(self):
        mat = Matrix( ((2,2),(2,2)) )
        vec = Vector( (3,3) )
        target = Vector( (12,12) )
        result = mat @ vec
        self.assertEqual(result, target)

    def test_matrix_matmul(self):
        m1 = Matrix( ((2,2),(2,2)) )
        m2 = Matrix( ((3,3),(3,3)) )
        target = Matrix( ((12,12),(12,12)) )
        result = m1 @ m2
        self.assertEqual(result, target)

    def test_vector_matmul_errshape(self):
        mat = Matrix( ((2,2),(2,2)) )
        vec = Vector( (3,3,3) )
        self.assertRaises(Exception, Matrix._vector_matmul, mat,vec)

    def test_matrix_matmul_errshape(self):
        m1 = Matrix( ((2,2),(2,2)) )
        m2 = Matrix( ((3,3),(3,3),(3,3)) )
        self.assertRaises(Exception, Matrix._matrix_matmul, m1, m2)

    def test_matrix_matmul_shape(self):
        m1 = Matrix( ((2,2),(2,2)) )
        m2 = Matrix( ((3,3,3),(3,3,3)))
        result = m1 @ m2
        self.assertEqual(result.shape, (2,3))

class TestMatrixProperties(unittest.TestCase):
    def test_matrix_row_vectors(self):
        matrix = Matrix( ((1,2),(3,4)))
        target = (Vector((1,2)), Vector((3,4)))
        result = matrix.row_vectors
        self.assertEqual(result, target)

    def test_matrix_col_vectors(self):
        matrix = Matrix( ((1,2),(3,4)) )
        target = (Vector((1,3)), Vector((2,4)))
        result = matrix.col_vectors
        self.assertEqual(result, target)

    def test_matrix_transpose(self):
        matrix = Matrix( ((1,2,3), (4,5,6)) )
        target = Matrix( ((1,4),(2,5),(3,6)) )
        result = matrix.transpose
        self.assertEqual(result, target)

    def test_matrix_is_square(self):
        matrix = Matrix( ((1,2),(3,4)) )
        target = True
        result = matrix.is_square
        self.assertEqual(result, target)

        matrix = Matrix( ((1,2,3),(4,5,6)) )
        target = False
        result = matrix.is_square
        self.assertEqual(result, target)

    def test_matrix_is_unitary(self):
        matrix = Matrix( ((1,0),(0,1)) )
        target = True
        result = matrix.is_unitary
        self.assertEqual(result,target)

        matrix = Matrix( ((1,1),(1,-1)) )
        target = False
        result = matrix.is_unitary
        self.assertEqual(result, target) 


class TestMathUtils(unittest.TestCase):
    def test_rad2deg(self):
        inputs = [0, pi/2, pi, 3*pi/2]
        targets = [0, 90, 180, 270]
        outputs = [math.rad2deg(x) for x in inputs]
        for (output, target) in zip(outputs,targets):
            self.assertEqual(output, target)

    def test_deg2rad(self):
        inputs = [0, 90, 180, 270]
        targets = [0, pi/2, pi, 3*pi/2]
        outputs = [math.deg2rad(x) for x in inputs]
        for (output, target) in zip(outputs, targets):
            self.assertEqual(output, target)

    def test_vec2d_to_angle(self):
        inputs = [
            [1,0],
            [0,1],
            [-1,0],
            [0,-1]
        ]
        targets = [0, 90, 180, 270]
        outputs = [math.vec2d_to_angle(x,y) for (x,y) in inputs]
        for (output, target) in zip(outputs, targets):
            self.assertEqual(output, target)
