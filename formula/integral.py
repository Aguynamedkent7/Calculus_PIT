import sympy as smp
import numpy as np

# bounded integral
def b_integral(user_input, symbol_wrt, lower_bound, upper_bound):
    fn = smp.parse_expr(user_input, {f'{symbol_wrt}': symbol_wrt})
    antiderivative = smp.integrate(fn, (symbol_wrt, lower_bound, upper_bound))
    return antiderivative

# unbounded integral
def ub_integral(user_input, symbol_wrt):
    fn = smp.parse_expr(user_input, {f'{symbol_wrt}': symbol_wrt})
    antiderivative = smp.integrate(fn, symbol_wrt)
    return antiderivative


# unbounded integral of range
def ub_integral_of_range(user_input, symbol_wrt, a, b):
    fn = smp.parse_expr(user_input, {f'{symbol_wrt}': symbol_wrt})
    antiderivative = smp.integrate(fn, symbol_wrt)
    lambda_antiderivative = smp.lambdify(symbol_wrt, antiderivative, modules=['numpy'])
    return lambda_antiderivative(np.array([i for i in range(a, b)]))

