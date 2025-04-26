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

    res = quad(lambda x: x, -np.inf, np.inf)
    print(res)


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

def ub_integral_of_range(user_input, symbol_wrt, a, b):
    """Return evaluated antiderivative function over a range"""
    try:
        if user_input.replace(".", "").isdigit():
            constant = float(user_input)
            return lambda x: constant * x

        fn = smp.parse_expr(user_input, {f'{symbol_wrt}': symbol_wrt})
        antiderivative = smp.integrate(fn, symbol_wrt)
        return careful_lambdify(symbol_wrt, antiderivative)
    except Exception as e:
        print(f"Error in integral of range: {e}")
        return lambda x: np.full_like(x, np.nan)

def careful_lambdify(symbol, expr):
    """Safe lambdify with NaN handling"""
    lambda_f = smp.lambdify(symbol, expr, modules=['numpy'])
    def safe_function(x):
        try:
            result = lambda_f(x)
            if isinstance(result, np.ndarray):
                result[~np.isfinite(result)] = np.linspace(np.nan, np.nan, 100)
            elif not np.isfinite(result):
                return np.linspace(np.nan, np.nan, 100)
            return result
        except:
            return np.linspace(np.nan, np.nan, 100)
    return np.vectorize(safe_function)


def scipy_integral_func(expr, symbol, a):
    """Returns a function F(x) = ∫_a^x f(t) dt using scipy.quad"""
    fn = smp.parse_expr(expr, {f'{symbol}': symbol})
    lambda_f = smp.lambdify(symbol, fn, modules=['numpy'])

    def integral_up_to_x(x_vals):
        x_vals = np.atleast_1d(x_vals)
        result = []
        for x in x_vals:
            try:
                val, _ = quad(lambda_f, a, x)
                result.append(val)
            except:
                result.append(np.nan)
        return np.array(result)

    return integral_up_to_x

        

if __name__ == '__main__':
    main()
