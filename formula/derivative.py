import sympy as smp
import numpy as np
from scipy.differentiate import derivative


def main():
    symbol = smp.symbols('x')
    print(numeric_derivative("x**2 + 6*x + 9", symbol, 1, 10, order=1))


def symbolic_derivative(user_input, symbol_wrt, order=1):
    try:
        # Handle pure numeric constants
        if user_input.replace(".", "").isdigit():
            return 0
        
        # Parse expression and handle symbolic constants
        fn = smp.parse_expr(user_input, {f'{symbol_wrt}': symbol_wrt})
        f_prime = smp.simplify(smp.diff(fn, symbol_wrt, order))
        return f_prime
    except Exception as e:
        print(f"Error in derivative: {e}")
        return None


def numeric_derivative(expr, symbol, a, b, order=1):
    """
    Returns a function that numerically computes the nth derivative of expr using finite differences.
    """
    x = np.linspace(a, b, 100)
    fn = smp.parse_expr(expr, {f'{symbol}': symbol})
    if order > 1:
        fn = smp.diff(fn, symbol, order-1)
    f = lambda x: smp.lambdify(symbol, fn, modules=["numpy"])(x)
    f_prime = derivative(f, x)
    return f_prime.df


if __name__ == '__main__':
    main()