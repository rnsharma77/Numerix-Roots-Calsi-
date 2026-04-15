"""
Secant Method for Root Finding
No derivative required. Uses two initial guesses.
Superlinear convergence (order ~1.618).
"""


def secant(f, x0, x1, tol=1e-6, max_iter=100):
    """
    Find root using Secant Method.

    Parameters:
        f       : callable, the function
        x0, x1  : float, two initial guesses
        tol     : float, tolerance
        max_iter: int, max iterations

    Returns:
        dict with keys: root, iterations, errors, history, converged, message
    """
    errors = []
    history = []

    for i in range(1, max_iter + 1):
        f0 = f(x0)
        f1 = f(x1)
        denom = f1 - f0

        if abs(denom) < 1e-14:
            return {
                "root": x1,
                "iterations": i,
                "errors": errors,
                "history": history,
                "converged": False,
                "message": f"Division by near-zero at iteration {i}. Method failed."
            }

        x2 = x1 - f1 * (x1 - x0) / denom
        error = abs(x2 - x1)

        errors.append(error)
        history.append({
            "iter": i,
            "root": x2,
            "f_root": f(x2),
            "error": error,
            "x0": x0,
            "x1": x1
        })

        x0, x1 = x1, x2

        if error < tol:
            return {
                "root": x2,
                "iterations": i,
                "errors": errors,
                "history": history,
                "converged": True,
                "message": f"Converged in {i} iterations. Root ≈ {x2:.8f}"
            }

    return {
        "root": x1,
        "iterations": max_iter,
        "errors": errors,
        "history": history,
        "converged": False,
        "message": f"Max iterations reached. Best root ≈ {x1:.8f}"
    }
