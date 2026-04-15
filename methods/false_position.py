"""
False Position (Regula Falsi) Method for Root Finding
Uses linear interpolation on interval [a, b].
Guaranteed convergence like bisection but often faster.
"""


def false_position(f, a, b, tol=1e-6, max_iter=100):
    """
    Find root of f(x) = 0 in interval [a, b] using False Position Method.

    Parameters:
        f       : callable, the function
        a, b    : float, interval endpoints (f(a)*f(b) < 0 required)
        tol     : float, tolerance for convergence
        max_iter: int, maximum iterations

    Returns:
        dict with keys: root, iterations, errors, history, converged, message
    """
    fa = f(a)
    fb = f(b)

    if fa * fb > 0:
        return {
            "root": None,
            "iterations": 0,
            "errors": [],
            "history": [],
            "converged": False,
            "message": "f(a) and f(b) must have opposite signs. No guaranteed root in [a, b]."
        }

    errors = []
    history = []
    root = None
    a_old = a
    b_old = b

    for i in range(1, max_iter + 1):
        # Linear interpolation
        if abs(fb - fa) < 1e-14:
            return {
                "root": b,
                "iterations": i,
                "errors": errors,
                "history": history,
                "converged": False,
                "message": "Function values too close. Method failed."
            }

        c = (a * fb - b * fa) / (fb - fa)
        fc = f(c)
        error = abs(c - root) if root is not None else abs(b - a)
        root = c

        errors.append(error)
        history.append({
            "iter": i,
            "a": a,
            "b": b,
            "root": c,
            "f_root": fc,
            "error": error
        })

        if abs(fc) < tol or error < tol:
            return {
                "root": c,
                "iterations": i,
                "errors": errors,
                "history": history,
                "converged": True,
                "message": f"Converged in {i} iterations. Root ≈ {c:.8f}"
            }

        if fa * fc < 0:
            b = c
            fb = fc
        else:
            a = c
            fa = fc

    return {
        "root": root,
        "iterations": max_iter,
        "errors": errors,
        "history": history,
        "converged": False,
        "message": f"Max iterations reached. Best root ≈ {root:.8f}"
    }
