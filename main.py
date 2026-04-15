"""
Web-based Root Finding Calculator
=================================
Browser UI built with Flask, HTML, and CSS while preserving the
existing numerical-method logic in Python.
"""

from __future__ import annotations

import base64
import io
from typing import Any

from flask import Flask, render_template, request

from utils.parser import parse_equation
from utils.graph import build_figure
from methods.bisection import bisection
from methods.newton import newton_raphson
from methods.secant import secant
from methods.false_position import false_position
from methods.fixed_point import fixed_point
from methods.mullers import mullers_method


app = Flask(__name__)


METHOD_INFO = {
    "Bisection": {
        "inputs": [("a", "a (left endpoint)"), ("b", "b (right endpoint)")],
        "description": "Guaranteed convergence by interval halving",
        "icon": "📊"
    },
    "False Position": {
        "inputs": [("a", "a (left endpoint)"), ("b", "b (right endpoint)")],
        "description": "Linear interpolation for faster convergence",
        "icon": "📈"
    },
    "Newton-Raphson": {
        "inputs": [("x0", "x0 (initial guess)")],
        "description": "Quadratic convergence, very fast",
        "icon": "⚡"
    },
    "Secant": {
        "inputs": [("x0", "x0 (first guess)"), ("x1", "x1 (second guess)")],
        "description": "No derivative needed, superlinear",
        "icon": "🎯"
    },
    "Muller's": {
        "inputs": [("x0", "x0 (first)"), ("x1", "x1 (second)"), ("x2", "x2 (third)")],
        "description": "Parabolic, highest order convergence",
        "icon": "✨"
    },
    "Fixed Point": {
        "inputs": [("x0", "x0 (initial)"), ("g", "g(x) function")],
        "description": "Custom iteration function",
        "icon": "🔄"
    },
}

EXAMPLES = [
    "x**3 - x - 2",
    "x**3 - 2*x - 5",
    "cos(x) - x",
    "sin(x)",
    "exp(x) - 3*x",
    "x**2 - 4",
    "log(x) - 1",
    "x**3 - x**2 - 1",
    "x**4 - 2*x**2 - 8",
    "tan(x) - x",
    "x - cos(x)",
    "exp(-x) - x",
]

DEFAULT_FORM = {
    "equation": "x**3 - x - 2",
    "method": "Bisection",
    "a": "1",
    "b": "2",
    "x0": "1.5",
    "x1": "2.0",
    "x2": "2.5",
    "g": "x",
    "tol": "1e-6",
    "max_iter": "100",
}

METHOD_DEFAULTS = {
    "Bisection": {"a": "1", "b": "2"},
    "False Position": {"a": "1", "b": "2"},
    "Newton-Raphson": {"x0": "1.5"},
    "Secant": {"x0": "1", "x1": "2"},
    "Muller's": {"x0": "1", "x1": "1.5", "x2": "2"},
    "Fixed Point": {"x0": "1.5", "g": "x"},
}


def _serialize_history(history: list[dict[str, Any]]) -> list[dict[str, Any]]:
    serialized = []
    for row in history:
        clean_row = {}
        for key, value in row.items():
            if isinstance(value, float):
                clean_row[key] = f"{value:.8f}"
            else:
                clean_row[key] = value
        serialized.append(clean_row)
    return serialized


def _figure_to_base64(fig) -> str:
    buffer = io.BytesIO()
    fig.savefig(buffer, format="png", dpi=150)
    fig.clf()
    buffer.seek(0)
    return base64.b64encode(buffer.read()).decode("ascii")


def _build_plot_data(f, result: dict[str, Any], method: str) -> str:
    fig = build_figure(
        f,
        result.get("root"),
        result.get("errors", []),
        method,
        a=result.get("_a"),
        b=result.get("_b"),
    )
    return _figure_to_base64(fig)


def _solve_request(form_data: dict[str, str]) -> dict[str, Any]:
    equation = form_data["equation"].strip()
    method = form_data["method"]

    f, df, cleaned_equation, parse_error = parse_equation(equation)
    if parse_error:
        raise ValueError(parse_error)

    try:
        tol = float(form_data["tol"])
        max_iter = int(form_data["max_iter"])
    except ValueError as exc:
        raise ValueError("Tolerance must be a float and max iterations must be an integer.") from exc

    try:
        if method == "Bisection":
            a_raw = form_data.get("a", "").strip()
            b_raw = form_data.get("b", "").strip()
            if not a_raw or not b_raw:
                raise ValueError("Please enter both interval values a and b for the Bisection method.")
            a = float(a_raw)
            b = float(b_raw)
            result = bisection(f, a, b, tol, max_iter)
            result["_a"] = a
            result["_b"] = b
        elif method == "False Position":
            a_raw = form_data.get("a", "").strip()
            b_raw = form_data.get("b", "").strip()
            if not a_raw or not b_raw:
                raise ValueError("Please enter both interval values a and b for the False Position method.")
            a = float(a_raw)
            b = float(b_raw)
            result = false_position(f, a, b, tol, max_iter)
            result["_a"] = a
            result["_b"] = b
        elif method == "Newton-Raphson":
            x0_raw = form_data.get("x0", "").strip()
            if not x0_raw:
                raise ValueError("Please enter the initial guess x0 for the Newton-Raphson method.")
            x0 = float(x0_raw)
            result = newton_raphson(f, df, x0, tol, max_iter)
            result["_a"] = None
            result["_b"] = None
        elif method == "Secant":
            x0_raw = form_data.get("x0", "").strip()
            x1_raw = form_data.get("x1", "").strip()
            if not x0_raw or not x1_raw:
                raise ValueError("Please enter both x0 and x1 for the Secant method.")
            x0 = float(x0_raw)
            x1 = float(x1_raw)
            result = secant(f, x0, x1, tol, max_iter)
            result["_a"] = None
            result["_b"] = None
        elif method == "Muller's":
            x0_raw = form_data.get("x0", "").strip()
            x1_raw = form_data.get("x1", "").strip()
            x2_raw = form_data.get("x2", "").strip()
            if not x0_raw or not x1_raw or not x2_raw:
                raise ValueError("Please enter all three guesses x0, x1, and x2 for Muller's method.")
            x0 = float(x0_raw)
            x1 = float(x1_raw)
            x2 = float(x2_raw)
            result = mullers_method(f, x0, x1, x2, tol, max_iter)
            result["_a"] = None
            result["_b"] = None
        elif method == "Fixed Point":
            x0_raw = form_data.get("x0", "").strip()
            g_str = form_data.get("g", "").strip()
            if not x0_raw or not g_str:
                raise ValueError("Please enter the initial guess x0 and the iteration function g(x).")
            x0 = float(x0_raw)
            g_func, _, _, g_err = parse_equation(g_str)
            if g_err:
                raise ValueError(f"Error parsing g(x): {g_err}")
            result = fixed_point(g_func, x0, tol, max_iter)
            result["_a"] = None
            result["_b"] = None
        else:
            raise ValueError("Unsupported method selected.")
    except ValueError:
        raise
    except Exception as exc:
        raise ValueError(str(exc)) from exc

    errors = result.get("errors", [])
    last_error = errors[-1] if errors else None

    return {
        "equation": cleaned_equation,
        "method": method,
        "root": result.get("root"),
        "iterations": result.get("iterations"),
        "converged": result.get("converged", False),
        "message": result.get("message", ""),
        "final_error": last_error,
        "history": _serialize_history(result.get("history", [])),
        "plot_image": _build_plot_data(f, result, method),
    }


@app.route("/", methods=["GET", "POST"])
def index():
    form_data = dict(DEFAULT_FORM)
    result = None
    error_message = None

    if request.method == "POST":
        for key in DEFAULT_FORM:
            form_data[key] = request.form.get(key, DEFAULT_FORM[key]).strip()

        for key, value in METHOD_DEFAULTS.get(form_data["method"], {}).items():
            if not form_data.get(key):
                form_data[key] = value

        try:
            result = _solve_request(form_data)
        except ValueError as exc:
            error_message = str(exc)

    return render_template(
        "index.html",
        method_info=METHOD_INFO,
        examples=EXAMPLES,
        form_data=form_data,
        result=result,
        error_message=error_message,
    )


if __name__ == "__main__":
    app.run(debug=True)
