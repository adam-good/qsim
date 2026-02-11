import unittest
import utils.math as math
import utils.gates as matrices
import numpy as np

class TestMathUtils(unittest.TestCase):
    def test_rad2deg(self):
        inputs = [0, np.pi/2, np.pi, 3*np.pi/2]
        targets = [0, 90, 180, 270]
        outputs = [math.rad2deg(x) for x in inputs]
        for (output, target) in zip(outputs,targets):
            self.assertEqual(output, target)

    def test_deg2rad(self):
        inputs = [0, 90, 180, 270]
        targets = [0, np.pi/2, np.pi, 3*np.pi/2]
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

class TestGateUtils(unittest.TestCase):
    def test_is_square(self):
        input = np.array([[1,2],[3,4]])
        target = True
        output = matrices.is_square(input)
        self.assertEqual(output, target)

        input = np.array([[1,2,3],[4,5,6]])
        target = False
        output = matrices.is_square(input)
        self.assertEqual(output, target)

    def test_is_unitary(self):
       input = np.array([[1,1],[1,-1]]) / np.sqrt(2)
       target = True
       output = matrices.is_unitary(input)
       self.assertEqual(output, target)

       input = np.array([[1,1],[1,-1]])
       target = False
       output = matrices.is_unitary(input)
       self.assertEqual(output, target)
       
