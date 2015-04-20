from PyCamellia import *
from ParseFunction import *
import unittest

x = 2.0
y = 3.0

class TestParseFunction(unittest.TestCase):

    """Test Add"""
    def test_add(self):
        func = stringToFunction("1+x")
        answ = 1 + x
        self.assertEqual(answ, func.evaluate(x))

    """Test Subtract"""
    def test_subtract(self):
        func = stringToFunction("3-x")
        answ = 3 - x
        self.assertEqual(answ, func.evaluate(x))

    """Test Divide"""
    def test_divide(self):
        func = stringToFunction("10/x")
        answ = 10 / x
        self.assertEqual(answ, func.evaluate(x))

    """Test Multiply"""
    def test_multiply(self):
        func = stringToFunction("2*x")
        answ = 2 * x
        self.assertEqual(answ, func.evaluate(x))

    """Test Exonent"""
    def test_exponent(self):
        func = stringToFunction("2^3")
        answ = 2 ** 3
        self.assertEqual(answ, func.evaluate(x))

    """Test Negative"""
    def test_negative(self):
        func = stringToFunction("x+-2")
        answ = x + -2
        self.assertEqual(answ, func.evaluate(x))

    """Test ParenMultiply"""
    def test_parenMultiply(self):
        func = stringToFunction("3(x)")
        answ = 3 * x
        self.assertEqual(answ, func.evaluate(x))

    """Test XandY"""
    def test_xAndY(self):
        global x
        global y
        func = stringToFunction("x+y")
        answ = x + y
        self.assertEqual(answ, func.evaluate(x, y))

    """Test NoParens"""
    def test_noParens(self):
        func = stringToFunction("5x^2y+2")
        answ = 5 * (x**2) * y + 2
        self.assertEqual(answ, func.evaluate(x, y))

    """Test Doubles"""
    def test_doubles(self):
        func = stringToFunction("2.0+5.0x*y^2")
        answ = 2.0 + 5.0 * x * y**2
        self.assertEqual(answ, func.evaluate(x, y))

    """Test HalfAssedDoubles"""
    def test_halfAssedDoubles(self):
        func = stringToFunction("2.+.6-x^2+y")
        answ = 2. + .6 - x**2 + y
        self.assertEqual(answ, func.evaluate(x, y))
        
    def test_RobertsInput(self):
        """Test input from Dr. Roberts"""
        func = stringToFunction("-3*(y-1)*(y-2)")
        answ = -3*(y-1)*(y-2)
        self.assertEqual(answ, func.evaluate(x, y))

    def test_RobertsInput2(self):
        """Test input from Dr. Roberts"""
        func = stringToFunction("-3*y*y+9*y-6")
        answ = -3*(y-1)*(y-2)
        self.assertEqual(answ, func.evaluate(x, y))

    """Test ePowerOfTen"""
    def test_ePowerOfTen(self):
        try:
            func = stringToFunction("xe2")
        except ValueError:
            error = True
        answ = x * 10 * 10
        #self.assertEqual(answ, func.evaluate(x))
        self.assertEqual(True, error)

    if __name__ == '__main__':
        unittest.main()
