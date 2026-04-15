"""
Newton-Raphson Method for Root Finding
Uses derivative: x_{n+1} = x_n - f(x_n)/f'(x_n)
Fast (quadratic) convergence but may fail with poor initial guess.
"""


def newton_raphson(f, df, x0, tol=1e-6, max_iter=100):
    """
    Find root using Newton-Raphson method.

    Parameters:
        f       : callable, the function
        df      : callable, derivative of f
        x0      : float, initial guess
        tol     : float, tolerance
        max_iter: int, max iterations

    Returns:
        dict with keys: root, iterations, errors, history, converged, message
    """
    errors = []
    history = []
    x = x0

    for i in range(1, max_iter + 1):
        fx = f(x)
        dfx = df(x)

        if abs(dfx) < 1e-14:
            return {
                "root": x,
                "iterations": i,
                "errors": errors,
                "history": history,
                "converged": False,
                "message": f"Derivative near zero at x = {x:.6f}. Method failed."
            }

        x_new = x - fx / dfx
        error = abs(x_new - x)

        errors.append(error)
        history.append({
            "iter": i,
            "root": x_new,
            "f_root": f(x_new),
            "error": error,
            "x_prev": x
        })

        x = x_new

        if error < tol:
            return {
                "root": x,
                "iterations": i,
                "errors": errors,
                "history": history,
                "converged": True,
                "message": f"Converged in {i} iterations. Root ≈ {x:.8f}"
            }

    return {
        "root": x,
        "iterations": max_iter,
        "errors": errors,
        "history": history,
        "converged": False,
        "message": f"Max iterations reached. Best root ≈ {x:.8f}"
    }
