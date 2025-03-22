import sympy as smp
import numpy as np


def main():
    symbol = smp.symbols('x')
    expr = "cbrt(8)"
    fn = smp.parse_expr(expr, {'x': symbol})
    f_prime = smp.diff(fn, symbol)
    print(fn)


def derivative_of_range(user_input, symbol_wrt, a, b, order=1):
    fn = smp.parse_expr(user_input, {f'{symbol_wrt}': symbol_wrt})
    f_prime = smp.diff(fn, symbol_wrt, order)
    lambda_f_prime = smp.lambdify(symbol_wrt, f_prime, modules=['numpy'])
    return lambda_f_prime(np.array([i for i in range(a, b)]))


def derivative(user_input, symbol_wrt, order=1):
    fn = smp.parse_expr(user_input, {f'{symbol_wrt}': symbol_wrt})
    f_prime = smp.diff(fn, symbol_wrt, order)
    return f_prime


if __name__ == '__main__':
    main()