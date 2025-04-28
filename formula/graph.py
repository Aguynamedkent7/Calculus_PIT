import numpy as np
import matplotlib.pyplot as plt
import sympy as sp
from formula.derivative import derivative_of_range
from formula.integral import ub_integral_of_range

def plot_function_and_result(expr_str, is_integral=False, x_range=(-10, 10)):
    symbol = sp.Symbol('x')

    # Convert expression to function
    fn = sp.sympify(expr_str)
    lambda_fn = sp.lambdify(symbol, fn, modules=['numpy'])

    # Generate x values
    x_vals = np.linspace(x_range[0], x_range[1], 400)
    y_vals = lambda_fn(x_vals)

    # Compute derivative or integral
    if is_integral:
        result_y_vals = ub_integral_of_range(expr_str, symbol, x_range[0], x_range[1])
        title = "Integral"
    else:
        result_y_vals = derivative_of_range(expr_str, symbol, x_range[0], x_range[1])
        title = "Derivative"

    # Plot the function and its result
    plt.figure(figsize=(8, 5))
    plt.plot(x_vals, y_vals, label=f"f(x) = {expr_str}", color="blue")
    plt.plot(x_vals, result_y_vals, label=f"{title} of f(x)", color="red", linestyle="dashed")
    plt.axhline(0, color="black", linewidth=0.5)
    plt.axvline(0, color="black", linewidth=0.5)
    plt.legend()
    plt.title(f"{title} of f(x)")
    plt.grid()
    plt.show()
