import sympy as smp
import numpy as np


def plot_og_func(user_input, symbol_wrt, x):
    try:
        if user_input.replace(".", "").isdigit():
            return float(user_input) * symbol_wrt

        fn = smp.parse_expr(user_input, {f'{symbol_wrt}': symbol_wrt})
        lambda_fn = smp.lambdify(symbol_wrt, fn)
        y_safe = np.where(np.isfinite(x), lambda_fn(x), np.nan)
        return y_safe
    
    except Exception as e:
        print(f"Error in plotting og func: {e}")
        return None