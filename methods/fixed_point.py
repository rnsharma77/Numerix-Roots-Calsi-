"""
Fixed Point Iteration Method for Root Finding
Converts f(x) = 0 into x = g(x) and iterates: x_{n+1} = g(x_n)
Convergence depends on |g'(x)| < 1 near root.
"""


def fixed_point(g, x0, tol=1e-6, max_iter=100):
    """
    Find fixed point of g(x) = x using Fixed Point Iteration.
    User should provide g such that f(x) = 0 becomes x = g(x).

    Parameters:
        g       : callable, iteration function (rearranged from f(x)=0)
        x0      : float, initial guess
        tol     : float, tolerance for convergence
        max_iter: int, maximum iterations

    Returns:
        dict with keys: root, iterations, errors, history, converged, message
    """
    errors = []
    history = []
    x = x0

    for i in range(1, max_iter + 1):
        try:
            x_new = g(x)
        except Exception as e:
            return {
                "root": x,
                "iterations": i,
                "errors": errors,
                "history": history,
                "converged": False,
                "message": f"Error evaluating g(x): {e}"
            }

        error = abs(x_new - x)

        errors.append(error)
        history.append({
            "iter": i,
            "root": x_new,
            "g_root": x_new,
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
                "message": f"Converged in {i} iterations. Fixed point ≈ {x:.8f}"
            }

    return {
        "root": x,
        "iterations": max_iter,
        "errors": errors,
        "history": history,
        "converged": False,
        "message": f"Max iterations reached. Best fixed point ≈ {x:.8f}"
    }
