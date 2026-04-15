"""
Muller's Method for Root Finding
Uses three points and fits a parabola. Can find complex roots.
Higher convergence order (~1.84) than secant.
"""

import math


def mullers_method(f, x0, x1, x2, tol=1e-6, max_iter=100):
    """
    Find root using Muller's Method.

    Parameters:
        f       : callable, the function
        x0, x1, x2 : float, three initial guesses
        tol     : float, tolerance
        max_iter: int, maximum iterations

    Returns:
        dict with keys: root, iterations, errors, history, converged, message
    """
    errors = []
    history = []

    for i in range(1, max_iter + 1):
        f0 = f(x0)
        f1 = f(x1)
        f2 = f(x2)

        # Divided differences
        h0 = x1 - x0
        h1 = x2 - x1

        if abs(h0) < 1e-14 or abs(h1) < 1e-14:
            return {
                "root": x2,
                "iterations": i,
                "errors": errors,
                "history": history,
                "converged": False,
                "message": "Points too close. Method failed."
            }

        delta0 = (f1 - f0) / h0
        delta1 = (f2 - f1) / h1
        a = (delta1 - delta0) / (h1 + h0)
        b = delta1 + h1 * a
        c = f2

        discriminant = b**2 - 4 * a * c
        if discriminant >= 0:
            sqrt_d = math.sqrt(discriminant)
        else:
            sqrt_d = math.sqrt(abs(discriminant)) * 1j  # Complex number

        if isinstance(sqrt_d, complex):
            # Return best real root so far
            return {
                "root": x2,
                "iterations": i,
                "errors": errors,
                "history": history,
                "converged": False,
                "message": f"Complex discriminant encountered at iter {i}. Best root ≈ {x2:.8f}"
            }

        denom1 = b + sqrt_d
        denom2 = b - sqrt_d
        denom = denom1 if abs(denom1) > abs(denom2) else denom2

        if abs(denom) < 1e-14:
            return {
                "root": x2,
                "iterations": i,
                "errors": errors,
                "history": history,
                "converged": False,
                "message": "Denominator near zero. Method failed."
            }

        x3 = x2 - 2 * c / denom
        error = abs(x3 - x2)

        errors.append(error)
        history.append({
            "iter": i,
            "root": x3,
            "f_root": f(x3),
            "error": error,
            "x0": x0,
            "x1": x1,
            "x2": x2
        })

        if error < tol:
            return {
                "root": x3,
                "iterations": i,
                "errors": errors,
                "history": history,
                "converged": True,
                "message": f"Converged in {i} iterations. Root ≈ {x3:.8f}"
            }

        x0, x1, x2 = x1, x2, x3

    return {
        "root": x2,
        "iterations": max_iter,
        "errors": errors,
        "history": history,
        "converged": False,
        "message": f"Max iterations reached. Best root ≈ {x2:.8f}"
    }
