import unittest
from utils.math.bit import Bit, BIT_0, BIT_1


class TestBit(unittest.TestCase):
    def test_bit_construction_valid(self):
        self.assertEqual(Bit(0).value, 0)
        self.assertEqual(Bit(1).value, 1)
        self.assertEqual(Bit(True).value, 1)
        self.assertEqual(Bit(False).value, 0)
    
    def test_bit_construction_invalid(self):
        with self.assertRaises(ValueError):
            Bit(2)
        with self.assertRaises(ValueError):
            Bit(-1)
        with self.assertRaises(ValueError):
            Bit(0.5)
        with self.assertRaises(ValueError):
            Bit(0.0)
        with self.assertRaises(ValueError):
            Bit(1.0)
        with self.assertRaises(ValueError):
            Bit("0")
        with self.assertRaises(ValueError):
            Bit(None)
    
    def test_bit_int_conversion(self):
        self.assertEqual(int(Bit(0)), 0)
        self.assertEqual(int(Bit(1)), 1)
    
    def test_bit_bool_conversion(self):
        self.assertIs(bool(Bit(0)), False)
        self.assertIs(bool(Bit(1)), True)
    
    def test_bit_index(self):
        self.assertEqual([0, 1][Bit(0)], 0)
        self.assertEqual([0, 1][Bit(1)], 1)
    
    def test_bit_add(self):
        self.assertEqual(Bit(0) + Bit(0), 0)
        self.assertEqual(Bit(0) + Bit(1), 1)
        self.assertEqual(Bit(1) + Bit(0), 1)
        self.assertEqual(Bit(1) + Bit(1), 0)
        self.assertEqual(Bit(1) + 1, 0)
        self.assertEqual(1 + Bit(1), 0)
    
    def test_bit_mul(self):
        self.assertEqual(Bit(0) * Bit(0), 0)
        self.assertEqual(Bit(0) * Bit(1), 0)
        self.assertEqual(Bit(1) * Bit(0), 0)
        self.assertEqual(Bit(1) * Bit(1), 1)
        self.assertEqual(Bit(1) * 0, 0)
        self.assertEqual(0 * Bit(1), 0)
    
    def test_bit_neg_pos(self):
        self.assertEqual(-Bit(0), 0)
        self.assertEqual(-Bit(1), 1)
        self.assertEqual(+Bit(0), 0)
        self.assertEqual(+Bit(1), 1)
    
    def test_bit_and(self):
        self.assertIs(Bit(0) & Bit(0), False)
        self.assertIs(Bit(0) & Bit(1), False)
        self.assertIs(Bit(1) & Bit(0), False)
        self.assertIs(Bit(1) & Bit(1), True)
        self.assertIs(Bit(1) & 0, False)
        self.assertIs(0 & Bit(1), False)
    
    def test_bit_or(self):
        self.assertIs(Bit(0) | Bit(0), False)
        self.assertIs(Bit(0) | Bit(1), True)
        self.assertIs(Bit(1) | Bit(0), True)
        self.assertIs(Bit(1) | Bit(1), True)
        self.assertIs(Bit(0) | 1, True)
        self.assertIs(1 | Bit(0), True)
    
    def test_bit_xor(self):
        self.assertIs(Bit(0) ^ Bit(0), False)
        self.assertIs(Bit(0) ^ Bit(1), True)
        self.assertIs(Bit(1) ^ Bit(0), True)
        self.assertIs(Bit(1) ^ Bit(1), False)
        self.assertIs(Bit(0) ^ 1, True)
        self.assertIs(1 ^ Bit(0), True)
    
    def test_bit_invert(self):
        self.assertEqual(~Bit(0), 1)
        self.assertEqual(~Bit(1), 0)
    
    def test_bit_equality(self):
        self.assertEqual(Bit(0), Bit(0))
        self.assertEqual(Bit(1), Bit(1))
        self.assertEqual(Bit(0), 0)
        self.assertEqual(Bit(1), 1)
        self.assertEqual(Bit(0), False)
        self.assertEqual(Bit(1), True)
        self.assertNotEqual(Bit(0), Bit(1))
        self.assertNotEqual(Bit(1), 0)
    
    def test_bit_hash(self):
        self.assertEqual(hash(Bit(0)), hash(0))
        self.assertEqual(hash(Bit(1)), hash(1))
        self.assertEqual({Bit(0), Bit(1)}, {0, 1})
        d = {Bit(0): "zero", Bit(1): "one"}
        self.assertEqual(d[Bit(0)], "zero")
        self.assertEqual(d[Bit(1)], "one")
    
    def test_bit_comparisons(self):
        self.assertTrue(Bit(0) < Bit(1))
        self.assertTrue(Bit(0) <= Bit(0))
        self.assertTrue(Bit(0) <= Bit(1))
        self.assertTrue(Bit(1) > Bit(0))
        self.assertTrue(Bit(1) >= Bit(1))
        self.assertTrue(Bit(1) >= Bit(0))
        self.assertTrue(Bit(0) < 1)
        self.assertTrue(Bit(1) > 0)
        self.assertTrue(0 <= Bit(1))
        self.assertTrue(1 >= Bit(0))
    
    def test_bit_repr(self):
        self.assertEqual(repr(Bit(0)), "Bit(value=0)")
        self.assertEqual(repr(Bit(1)), "Bit(value=1)")
    
    def test_bit_constants(self):
        self.assertEqual(BIT_0.value, 0)
        self.assertEqual(BIT_1.value, 1)
        self.assertIs(BIT_0, BIT_0)
        self.assertIs(BIT_1, BIT_1)
        self.assertEqual(BIT_0, Bit(0))
        self.assertEqual(BIT_1, Bit(1))


if __name__ == "__main__":
    unittest.main()