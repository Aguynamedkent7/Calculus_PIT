import numpy as np
import sympy as smp
import matplotlib.pyplot as plt

symbol = smp.symbols('x')
expr = "-log(cos(x))"
lambda_func = smp.lambdify(symbol, expr, modules='numpy')

x_vals = np.linspace(0, 10, 100)
y_vals = lambda_func(x_vals)

# Handle invalid values (e.g., cos(x) <= 0)
with np.errstate(invalid="ignore"):
    y_vals_safe = np.where(np.cos(x_vals) > 0, y_vals, np.nan)

# Plot the valid values
plt.plot(x_vals, y_vals_safe, label="Function with NaN for invalid values")
plt.xlabel("x")
plt.ylabel("y")
plt.title("Graph of -log(cos(x)) with NaN Handling")
plt.legend()
plt.grid()
plt.show()