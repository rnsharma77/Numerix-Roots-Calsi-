"""
Equation parser: converts a user-entered string into callable f(x) and f'(x).
Uses sympy for symbolic differentiation, with a safe eval fallback.
Enhanced to support more functions and better error handling.
"""

import math

# Try to import sympy for symbolic differentiation
try:
    import sympy as sp
    SYMPY_AVAILABLE = True
except ImportError:
    SYMPY_AVAILABLE = False

# Safe namespace for eval - Extended with more functions
SAFE_NAMESPACE = {
    "x": 0,
    # Trigonometric
    "sin": math.sin, "cos": math.cos, "tan": math.tan,
    "asin": math.asin, "acos": math.acos, "atan": math.atan,
    # Hyperbolic
    "sinh": math.sinh, "cosh": math.cosh, "tanh": math.tanh,
    "asinh": math.asinh, "acosh": math.acosh, "atanh": math.atanh,
    # Exponential and Logarithmic
    "exp": math.exp, "log": math.log, "log10": math.log10, "log2": math.log2,
    # Power and Root
    "sqrt": math.sqrt, "pow": math.pow,
    # Absolute, min, max
    "abs": abs, "fabs": math.fabs, "min": min, "max": max,
    # Constants
    "pi": math.pi, "e": math.e, "tau": math.tau, "inf": math.inf,
    # Other
    "ceil": math.ceil, "floor": math.floor, "factorial": math.factorial,
    "degrees": math.degrees, "radians": math.radians,
    "__builtins__": {}
}


def parse_equation(expr_str):
    """
    Parse a string equation into (f, df, expr_latex).

    Parameters:
        expr_str : str, e.g. "x**3 - x - 2"

    Returns:
        f        : callable, f(x)
        df       : callable, f'(x) (symbolic if sympy available, else numerical)
        expr_str : str, cleaned expression
        error    : str or None, error message if parsing failed
    """
    expr_str = expr_str.strip()

    # Basic replacements for user convenience
    expr_str = expr_str.replace("^", "**")

    # Test parse
    try:
        ns = dict(SAFE_NAMESPACE)
        ns["x"] = 1.0
        eval(compile(expr_str, "<string>", "eval"), {"__builtins__": {}}, ns)
    except Exception as e:
        return None, None, expr_str, f"Could not parse equation: {e}"

    def f(x_val):
        ns = dict(SAFE_NAMESPACE)
        ns["x"] = float(x_val)
        return float(eval(compile(expr_str, "<string>", "eval"), {"__builtins__": {}}, ns))

    if SYMPY_AVAILABLE:
        try:
            x_sym = sp.Symbol("x")
            expr_sym = sp.sympify(expr_str, locals={"x": x_sym})
            deriv_sym = sp.diff(expr_sym, x_sym)
            deriv_func = sp.lambdify(x_sym, deriv_sym, modules=["math"])

            def df(x_val):
                return float(deriv_func(float(x_val)))

        except Exception:
            df = _numerical_derivative(f)
    else:
        df = _numerical_derivative(f)

    return f, df, expr_str, None


def _numerical_derivative(f, h=1e-7):
    """Central difference numerical derivative."""
    def df(x):
        return (f(x + h) - f(x - h)) / (2 * h)
    return df
