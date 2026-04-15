"""
Bisection Method for Root Finding
Works on interval [a, b] where f(a) and f(b) have opposite signs.
Guaranteed convergence but slow (linear).
"""


def bisection(f, a, b, tol=1e-6, max_iter=100):
    """
    Find root of f(x) = 0 in interval [a, b] using Bisection Method.

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
    history = []  # list of (iteration, a, b, midpoint, f(mid), error)
    root = None

    for i in range(1, max_iter + 1):
        mid = (a + b) / 2.0
        fmid = f(mid)
        error = abs(b - a) / 2.0

        errors.append(error)
        history.append({
            "iter": i,
            "a": a,
            "b": b,
            "root": mid,
            "f_root": fmid,
            "error": error
        })

        if error < tol or fmid == 0.0:
            root = mid
            return {
                "root": root,
                "iterations": i,
                "errors": errors,
                "history": history,
                "converged": True,
                "message": f"Converged in {i} iterations. Root ≈ {mid:.8f}"
            }

        if fa * fmid < 0:
            b = mid
            fb = fmid
        else:
            a = mid
            fa = fmid

    root = (a + b) / 2.0
    return {
        "root": root,
        "iterations": max_iter,
        "errors": errors,
        "history": history,
        "converged": False,
        "message": f"Max iterations reached. Best root ≈ {root:.8f}"
    }
