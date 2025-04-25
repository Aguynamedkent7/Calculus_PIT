import sympy as smp
import numpy as np

def b_integral(user_input, symbol_wrt, lower_bound, upper_bound):
    """Bounded integral with error handling and constant support"""
    try:
        # Handle pure numeric constants
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
    """Unbounded integral with error handling and constant support"""
    try:
        # Handle pure numeric constants
        if user_input.replace(".", "").isdigit():
            return float(user_input) * symbol_wrt
        
        fn = smp.parse_expr(user_input, {f'{symbol_wrt}': symbol_wrt})
        antiderivative = smp.integrate(fn, symbol_wrt)
        return smp.simplify(antiderivative)
    except Exception as e:
        print(f"Error in unbounded integral: {e}")
        return None

def ub_integral_of_range(user_input, symbol_wrt, a, b):
    """Unbounded integral over a range with vectorization support"""
    try:
        # Handle pure numeric constants
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
    """Handle potential division by zero and complex numbers"""
    lambda_f = smp.lambdify(symbol, expr, modules=['numpy'])
    
    def safe_function(x):
        try:
            result = lambda_f(x)
            if isinstance(result, np.ndarray):
                result[~np.isfinite(result)] = np.nan
            elif not np.isfinite(result):
                return np.nan
            return result
        except:
            return np.nan
    
    return np.vectorize(safe_function)

def main():
    """Test the integral functions"""
    symbol = smp.symbols('x')
    test_cases = [
        "0",           # numeric constant
        "pi",         # symbolic constant
        "2*pi",       # symbolic constant with coefficient
        "x",          # linear
        "x^2",        # quadratic
        "1/x",        # rational
        "sin(x)"      # trigonometric
    ]
    
    print("Testing integrals:")
    for expr in test_cases:
        ub_result = ub_integral(expr, symbol)
        b_result = b_integral(expr, symbol, 0, 1)
        print(f"∫({expr})dx = {ub_result}")
        print(f"∫[0 to 1]({expr})dx = {b_result}")
        print("-" * 40)

if __name__ == '__main__':
    main()

