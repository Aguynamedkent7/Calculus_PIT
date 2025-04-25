import sympy as smp
import numpy as np



def main():
    symbol = smp.symbols('x')
    # Test cases for constants
    test_cases = [
        "5",           # numeric constant
        "pi",         # symbolic constant
        "2*pi",       # symbolic constant with coefficient
        "x",          # linear
        "x + 3",      # linear + constant
        "pi*x",       # symbolic constant * variable
    ]
    
    print("Testing derivatives:")
    for expr in test_cases:
        # result = derivative_of_range(expr, symbol, 1, 10)
        
        print(f"d/dx({expr}) = {smp.diff(expr, symbol)}")


def derivative(user_input, symbol_wrt, order=1):
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


def scipy_derivative_func(expr, symbol, order=1):
    """
    Returns a function that numerically computes the nth derivative of expr using finite differences.
    """
    fn = smp.parse_expr(expr, {f'{symbol}': symbol})
    lambda_f = smp.lambdify(symbol, fn, modules=["numpy"])

    def nth_derivative(x_vals):
        x_vals = np.atleast_1d(x_vals)
        h = 1e-5  # small step size for finite difference
        x_vals = np.asarray(x_vals)
        result = np.zeros_like(x_vals, dtype=float)

        for i, x in enumerate(x_vals):
            try:
                val = lambda_f
                for _ in range(order):
                    # Apply central difference for derivative
                    val = (lambda x: (val(x + h) - val(x - h)) / (2 * h))
                result[i] = val(x)
            except:
                result[i] = np.nan
        return result

    return nth_derivative


def derivative_of_range(user_input, symbol_wrt, a, b, order=1):
    try:
        # Handle pure numeric constants
        if user_input.replace(".", "").isdigit():
            return lambda x: np.zeros_like(x)
        
        fn = smp.parse_expr(user_input, {f'{symbol_wrt}': symbol_wrt})
        f_prime = smp.diff(fn, symbol_wrt, order)
        lambda_f_prime = careful_lambdify(symbol_wrt, f_prime)
        return lambda_f_prime
    except Exception as e:
        print(f"Error in derivative_of_range: {e}")
        return lambda x: None


def careful_lambdify(symbol, expr):
    """Handle potential division by zero and complex numbers"""
    lambda_f = smp.lambdify(symbol, expr, modules=['numpy'])
    
    def safe_function(x):
        try:
            result = lambda_f(x)
            # Handle array inputs
            if isinstance(x, np.ndarray):
                if isinstance(result, np.ndarray):
                    result[~np.isfinite(result)] = np.nan
                    return result
                elif not np.isfinite(result):
                    return np.full_like(x, np.nan)
                return result
            # Handle scalar inputs
            if not np.isfinite(result):
                return np.full_like(x, np.nan)
            return result
        except:
            if isinstance(x, np.ndarray):
                return np.full_like(x, np.nan)
            return np.nan
    
    return np.vectorize(safe_function)


if __name__ == '__main__':
    main()