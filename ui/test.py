import numpy as np
import sympy as smp
import matplotlib.pyplot as plt
from scipy.differentiate import derivative

# Define the function
def f(x):
    fn = smp.parse_expr("x**2 + 3/ x**3 - 1")
    return smp.lambdify(smp.symbols('x'), fn, modules=['numpy'])(x)

# Define the range of x values
x = np.linspace(-50, 50, 100)

# Compute the derivative using scipy.differentiate.derivative
dy_dx = derivative(f, x)
# Plot the original function
plt.plot(x, f(x), label="f(x)", color="blue")

# Plot the derivative
plt.plot(x, dy_dx.df, label="f'(x)", color="red")

# Add labels, legend, and grid
plt.title("Function and its Derivative")
plt.xlabel("x")
plt.ylabel("y")
plt.legend()
plt.grid()

# Show the plot
plt.show()