import utils.math as math
from math import pi
import unittest




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
