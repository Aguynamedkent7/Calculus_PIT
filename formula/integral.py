import sympy as smp
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import quad


def main():
    symbol = smp.symbols('x')
    test_cases = [
        "0",
        "pi",
        "2*pi",
        "x",
        "x^2",
        "1/x",
        "sin(x)"
    ]

    print("Testing integrals:")
    # for expr in test_cases:
    #     fixed_expr = expr.replace("^", "**")
    #     ub_result = ub_integral(fixed_expr, symbol)
    #     b_result = b_integral(fixed_expr, symbol, 0, 1)
    #     print(f"∫({expr}) dx = {ub_result}")
    #     print(f"∫₀¹({expr}) dx = {b_result}")
    #     print("-" * 40)



def b_integral(user_input, symbol_wrt, lower_bound, upper_bound):
    """Bounded integral with symbolic evaluation"""
    try:
        if user_input.replace(".", "").isdigit():
            constant = float(user_input)
            return constant * (upper_bound - lower_bound)

        fn = smp.parse_expr(user_input, {f'{symbol_wrt}': symbol_wrt})
        antiderivative = smp.integrate(fn, (symbol_wrt, lower_bound, upper_bound))
        return smp.simplify(antiderivative)
    except Exception as e:
        print(f"Error in bounded integral: {e}")
        return None

def ub_integral(user_input, symbol_wrt):
    """Unbounded integral with symbolic result"""
    try:
        if user_input.replace(".", "").isdigit():
            return float(user_input) * symbol_wrt

        fn = smp.parse_expr(user_input, {f'{symbol_wrt}': symbol_wrt})
        antiderivative = smp.integrate(fn, symbol_wrt)
        return smp.simplify(antiderivative)
    except Exception as e:
        print(f"Error in unbounded integral: {e}")
        return None


def ub_integral_of_range(user_input, symbol_wrt, x):
    try:
        if user_input.replace(".", "").isdigit():
            return float(user_input) * symbol_wrt

        fn = smp.parse_expr(user_input, {f'{symbol_wrt}': symbol_wrt})
        antiderivative = smp.integrate(fn, symbol_wrt)
        lambda_antiderivative = smp.lambdify(symbol_wrt, antiderivative)
        y_safe = np.where(np.isfinite(x), lambda_antiderivative(x), np.nan)
        return y_safe
    
    except Exception as e:
        print(f"Error in unbounded integral: {e}")
        return None

        

if __name__ == '__main__':
    main()
