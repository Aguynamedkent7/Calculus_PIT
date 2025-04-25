import numpy as np
import matplotlib.pyplot as plt
from scipy.differentiate import derivative

# Define the function
def f(x):
    return x**3 - 3*x**2 + 2*x

# Define the range of x values
x = np.linspace(-1, 3, 100)

# Compute the derivative using scipy.differentiate.derivative
dy_dx = derivative(f, x)
# Plot the original function
plt.plot(x, f(x), label="f(x)", color="blue")

# Plot the derivative
plt.plot(x, dy_dx.df, label="f'(x)", color="red", linestyle="--")

# Add labels, legend, and grid
plt.title("Function and its Derivative")
plt.xlabel("x")
plt.ylabel("y")
plt.legend()
plt.grid()

# Show the plot
plt.show()