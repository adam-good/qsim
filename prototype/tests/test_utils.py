from utils.typing import Vector
import unittest

class TestVector(unittest.TestCase):
    def test_add(self):
        v1 = Vector((1,2))
        v2 = Vector((3,4))
        target = Vector((4,6))
        result = v1+v2
        self.assertEqual(result, target)

    def test_sub(self):
        v1 = Vector((1,2))
        v2 = Vector((3,4))
        target = Vector((-2, -2))
        result = v1-v2
        self.assertEqual(result, target)

    def test_mul(self):
        v1 = Vector((1,2))
        v2 = Vector((3,4))
        target = Vector((3,8))
        result = v1*v2
        self.assertEqual(result, target)

    def test_div(self):
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

# class TestMathUtils(unittest.TestCase):
#     def test_rad2deg(self):
#         inputs = [0, pi/2, pi, 3*pi/2]
#         targets = [0, 90, 180, 270]
#         outputs = [qmath.rad2deg(x) for x in inputs]
#         for (output, target) in zip(outputs,targets):
#             self.assertEqual(output, target)

#     def test_deg2rad(self):
#         inputs = [0, 90, 180, 270]
#         targets = [0, pi/2, pi, 3*pi/2]
#         outputs = [qmath.deg2rad(x) for x in inputs]
#         for (output, target) in zip(outputs, targets):
#             self.assertEqual(output, target)

#     def test_vec2d_to_angle(self):
#         inputs = [
#             [1,0],
#             [0,1],
#             [-1,0],
#             [0,-1]
#         ]
#         targets = [0, 90, 180, 270]
#         outputs = [qmath.vec2d_to_angle(x,y) for (x,y) in inputs]
#         for (output, target) in zip(outputs, targets):
#             self.assertEqual(output, target)

# class TestGateUtils(unittest.TestCase):
#     def test_is_square(self):
#         input = np.array([[1,2],[3,4]])
#         target = True
#         output = matrices.is_square(input)
#         self.assertEqual(output, target)

#         input = np.array([[1,2,3],[4,5,6]])
#         target = False
#         output = matrices.is_square(input)
#         self.assertEqual(output, target)

#     def test_is_unitary(self):
#        input = np.array([[1,1],[1,-1]]) / np.sqrt(2)
#        target = True
#        output = matrices.is_unitary(input)
#        self.assertEqual(output, target)

#        input = np.array([[1,1],[1,-1]])
#        target = False
#        output = matrices.is_unitary(input)
#        self.assertEqual(output, target)
       
