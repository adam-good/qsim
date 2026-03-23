import unittest
import math
import utils.math as umath

class TestMathUtils(unittest.TestCase):
    def test_rad2deg(self):
        inputs = [0, math.pi/2, math.pi, 3*math.pi/2]
        targets = [0, 90, 180, 270]
        outputs = [umath.rad2deg(x) for x in inputs]
        for (output, target) in zip(outputs,targets):
            self.assertEqual(output, target)

    def test_deg2rad(self):
        inputs = [0, 90, 180, 270]
        targets = [0, math.pi/2, math.pi, 3*math.pi/2]
        outputs = [umath.deg2rad(x) for x in inputs]
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
        outputs = [umath.vec2d_to_angle(x,y) for (x,y) in inputs]
        for (output, target) in zip(outputs, targets):
            self.assertEqual(output, target)

if __name__ == "__main__":
    unittest.main()
