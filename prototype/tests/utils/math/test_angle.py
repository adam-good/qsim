import unittest

from src.utils.math.angle import Angle


class TestAngle(unittest.TestCase):
    def test_angle_construction(self):
        self.assertEqual(Angle(90).value, 90.0)
