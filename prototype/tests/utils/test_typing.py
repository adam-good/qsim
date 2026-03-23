import unittest
import utils.typing as types

class TestVector(unittest.TestCase):
    def test_scalar_add(self):
        vector = types.Vector((1,2))
        scalar = 2.
        target = types.Vector((3,4))
        result = vector + scalar
        self.assertEqual(result, target)

    def test_vector_add(self):
        v1 = types.Vector((1,2))
        v2 = types.Vector((3,4))
        target = types.Vector((4,6))
        result = v1+v2
        self.assertEqual(result, target)

    def test_scalar_sub(self):
        vector = types.Vector((1,2))
        scalar = 2.
        target = types.Vector((-1,0))
        result = vector - scalar
        self.assertEqual(result, target)
        
    def test_vector_sub(self):
        v1 = types.Vector((1,2))
        v2 = types.Vector((3,4))
        target = types.Vector((-2, -2))
        result = v1-v2
        self.assertEqual(result, target)

    def test_scalar_mul(self):
        vector = types.Vector((1,2))
        scalar = 2.
        target = types.Vector((2,4))
        result = vector * scalar
        self.assertEqual(result, target)
        
    def test_vector_mul(self):
        v1 = types.Vector((1,2))
        v2 = types.Vector((3,4))
        target = types.Vector((3,8))
        result = v1*v2
        self.assertEqual(result, target)


    def test_scalar_div(self):
        vector = types.Vector((1,2))
        scalar = 2.
        target = types.Vector((1/2,2/2))
        result = vector / scalar
        self.assertEqual(result, target)

    def test_vector_div(self):
        v1 = types.Vector((1,2))
        v2 = types.Vector((3,4))
        target = types.Vector((1/3, 2/4))
        result = v1/v2
        self.assertEqual(result, target)

    def test_pow(self):
        vec = types.Vector((1,2))
        scalar = 3
        target = types.Vector((1, 8))
        result = vec ** scalar
        self.assertEqual(result, target)

    def test_dotprod(self):
        v1 = types.Vector((1,2))
        v2 = types.Vector((3,4))
        target = 11
        result = types.Vector.dotprod(v1,v2)
        self.assertEqual(result,target)



class TestMatrixArithmatic(unittest.TestCase):
    def test_scalar_add(self):
        matrix = types.Matrix( ((1,2),(3,4)) )
        scalar = 2.
        target = types.Matrix( ((3,4),(5,6)) )
        result = matrix+scalar
        self.assertEqual(result, target)

    def test_scalar_sub(self):
        matrix = types.Matrix( ((1,2),(3,4)) )
        scalar = 2.
        target = types.Matrix( ((-1,0),(1,2)) )
        result = matrix - scalar
        self.assertEqual(result, target)

    def test_scalar_mul(self):
        matrix = types.Matrix( ((1,2),(3,4)) )
        scalar = 2.
        target = types.Matrix( ((2,4),(6,8)) )
        result = matrix * scalar
        self.assertEqual(result, target)

    def test_scalar_div(self):
        matrix = types.Matrix( ((1,2),(3,4)) )
        scalar = 2.
        target = types.Matrix( ((1/2,2/2),(3/2,4/2)) )
        result = matrix / scalar
        self.assertEqual(result, target)

    def test_elementwise_add(self):
        m1 = types.Matrix( ((3,3),(3,3)) )
        m2 = types.Matrix( ((2,2),(2,2)))
        target = types.Matrix( ((5,5),(5,5)) )
        result = m1+m2
        self.assertEqual(result, target)

    def test_elementwise_sub(self):
        m1 = types.Matrix( ((3,3),(3,3)) )
        m2 = types.Matrix( ((2,2),(2,2)) )
        target = types.Matrix( ((1,1),(1,1)) )
        result = m1 - m2
        self.assertEqual(result, target)

    def test_elementwise_mul(self):
        m1 = types.Matrix( ((3,3),(3,3)) )
        m2 = types.Matrix( ((2,2),(2,2)) )
        target = types.Matrix( ((6,6),(6,6)) )
        result = m1 * m2
        self.assertEqual(result, target)

    def test_elementwise_div(self):
        m1 = types.Matrix( ((3,3),(3,3)) )
        m2 = types.Matrix( ((2,2),(2,2)) )
        target = types.Matrix( ((3/2,3/2),(3/2,3/2)) )
        result = m1 / m2
        self.assertEqual(result, target)

    def test_vector_matmul(self):
        mat = types.Matrix( ((2,2),(2,2)) )
        vec = types.Vector( (3,3) )
        target = types.Vector( (12,12) )
        result = mat @ vec
        self.assertEqual(result, target)

    def test_matrix_matmul(self):
        m1 = types.Matrix( ((2,2),(2,2)) )
        m2 = types.Matrix( ((3,3),(3,3)) )
        target = types.Matrix( ((12,12),(12,12)) )
        result = m1 @ m2
        self.assertEqual(result, target)

    def test_vector_matmul_errshape(self):
        mat = types.Matrix( ((2,2),(2,2)) )
        vec = types.Vector( (3,3,3) )
        self.assertRaises(Exception, types.Matrix._vector_matmul, mat,vec)

    def test_matrix_matmul_errshape(self):
        m1 = types.Matrix( ((2,2),(2,2)) )
        m2 = types.Matrix( ((3,3),(3,3),(3,3)) )
        self.assertRaises(Exception, types.Matrix._matrix_matmul, m1, m2)

    def test_matrix_matmul_shape(self):
        m1 = types.Matrix( ((2,2),(2,2)) )
        m2 = types.Matrix( ((3,3,3),(3,3,3)))
        result = m1 @ m2
        self.assertEqual(result.shape, (2,3))

class TestMatrixProperties(unittest.TestCase):
    def test_matrix_row_vectors(self):
        matrix = types.Matrix( ((1,2),(3,4)))
        target = (types.Vector((1,2)), types.Vector((3,4)))
        result = matrix.row_vectors()
        self.assertEqual(result, target)

    def test_matrix_col_vectors(self):
        matrix = types.Matrix( ((1,2),(3,4)) )
        target = (types.Vector((1,3)), types.Vector((2,4)))
        result = matrix.col_vectors()
        self.assertEqual(result, target)

    def test_matrix_transpose(self):
        matrix = types.Matrix( ((1,2,3), (4,5,6)) )
        target = types.Matrix( ((1,4),(2,5),(3,6)) )
        result = matrix.transpose()
        self.assertEqual(result, target)

    def test_matrix_is_square(self):
        matrix = types.Matrix( ((1,2),(3,4)) )
        target = True
        result = matrix.is_square()
        self.assertEqual(result, target)

        matrix = types.Matrix( ((1,2,3),(4,5,6)) )
        target = False
        result = matrix.is_square()
        self.assertEqual(result, target)

    def test_matrix_is_unitary(self):
        matrix = types.Matrix( ((1,0),(0,1)) )
        target = True
        result = matrix.is_unitary()
        self.assertEqual(result,target)

        matrix = types.Matrix( ((1,1),(1,-1)) )
        target = False
        result = matrix.is_unitary()
        self.assertEqual(result, target) 

if __name__ == "__main__":
    unittest.main()
