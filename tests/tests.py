import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import sympy as smp
import numpy as np
from numpy.testing import assert_array_equal
from formula.derivative import derivative_of_range, derivative

NORMAL_FN = "x**2 + 6*x + 9"
MULTIPLICATION_FN = "x**2 * 6*x * 9"
DIV_FN = "(3x**3 + 10*x**2) / 6*x"
CHAIN_RULE_FN = "2*x*(3*x**2)**2"
SYMBOL_WRT = smp.symbols('x', real=True)


def test_derivative():
    # test for normal function
    result = derivative(NORMAL_FN, SYMBOL_WRT, 1)
    expected = "2*x + 6"  # Replace with the actual expected result
    assert str(result) == expected, f"Expected {expected}, got {result}"


def test_higher_order_derivative():
    # 2nd order derivative
    result = derivative(NORMAL_FN, SYMBOL_WRT, 2)
    expected = "2"  # Replace with the actual expected result
    assert str(result) == expected, f"Expected {expected}, got {result}"

    # 3rd order derivative
    result = derivative(NORMAL_FN, SYMBOL_WRT, 3)
    expected = "0"  # Replace with the actual expected result
    assert str(result) == expected, f"Expected {expected}, got {result}"


def test_derivative_of_range():
    # test for normal function with range
    result = derivative_of_range(NORMAL_FN, SYMBOL_WRT, 1, 10)
    expected = np.array([8, 10, 12, 14, 16, 18, 20, 22, 24])  # Replace with the actual expected result
    assert_array_equal(result, expected, err_msg=f"Expected {expected}, got {result}")


def test_higher_order_derivative_of_range():
    # 2nd derivative
    result = derivative_of_range(NORMAL_FN, SYMBOL_WRT, 1, 10, 2)
    expected = [2]  # Replace with the actual expected result
    assert_array_equal(result, expected, err_msg=f"Expected {expected}, got {result}")

    # 3rd derivative
    result = derivative_of_range(NORMAL_FN, SYMBOL_WRT, 1, 10, 3)
    expected = [0]  # Replace with the actual expected result
    assert_array_equal(result, expected, err_msg=f"Expected {expected}, got {result}")