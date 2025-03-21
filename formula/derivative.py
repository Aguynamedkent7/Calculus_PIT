import sympy as smp

x, y, z = smp.symbols('x y z', real=True)

f = smp.diff(x**2 + 2*x + 1, x)
print(f)