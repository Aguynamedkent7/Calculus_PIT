import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import sympy as smp
import numpy as np
from numpy.testing import assert_almost_equal
from formula.integral import b_integral, ub_integral, ub_integral_of_range

NORMAL_FN = "x**2 + 6*x + 9"
SYMBOL_WRT = smp.symbols('x', real=True)

def test_b_integral():
    result = b_integral(NORMAL_FN, SYMBOL_WRT, 0, 1)
    expected = "37/3"  # Replace with the actual expected result
    assert str(result) == expected, f"Expected {expected}, got {result}"

def test_ub_integral():
    result = ub_integral(NORMAL_FN, SYMBOL_WRT)
    expected = "x**3/3 + 3*x**2 + 9*x"  # Replace with the actual expected result
    assert str(result) == expected, f"Expected {expected}, got {result}"


def test_ub_integral_of_range():
    result = ub_integral_of_range(NORMAL_FN, SYMBOL_WRT, 1, 10)
    expected = np.array([12.33, 32.66, 63, 
                         105.33, 161.66, 234, 
                         324.33, 434.66, 567])  # Replace with the actual expected result
    assert_almost_equal(result, expected, decimal=2, err_msg=f"Expected {expected}, got {result}")