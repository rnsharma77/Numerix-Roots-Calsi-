# Technical Documentation

## Overview

This project is a server-rendered Flask application for root finding. A browser form collects the equation, numerical method, and method parameters. The backend parses the equation, runs the selected algorithm, generates a matplotlib figure, serializes iteration history, and returns the results to the template for display.

## Architecture

```text
Browser
  |
  v
templates/index.html + static/style.css
  |
  v
main.py (Flask route, validation, orchestration)
  |
  +--> utils/parser.py   -> parse equation and derivative
  +--> methods/*.py      -> run selected root-finding method
  +--> utils/graph.py    -> generate function/convergence plot
  |
  v
Rendered HTML with metrics, plot image, and iteration table
```

## Request Flow

1. The user submits the form on `/`.
2. `main.py:index()` copies request values into `form_data`.
3. `_solve_request()` parses the equation and validates tolerance and iteration count.
4. The selected method implementation is called from `methods/`.
5. The solver result is normalized into a response dictionary.
6. `utils/graph.build_figure()` creates a two-panel matplotlib figure.
7. The figure is converted to base64 and embedded directly into the HTML response.
8. The template displays status, metrics, iteration history, and the generated plot.

## Core Modules

### `main.py`

Responsibilities:

- Creates the Flask app
- Defines available methods and their required inputs
- Accepts `GET` and `POST` requests on `/`
- Parses and validates submitted values
- Dispatches the selected numerical method
- Serializes floating-point history rows for table display
- Generates plot output as a base64 PNG string

Important data structures:

- `METHOD_INFO`
  - UI-facing metadata for labels, descriptions, icons, and required parameters
- `DEFAULT_FORM`
  - Default values shown when the page first loads
- `METHOD_DEFAULTS`
  - Fallback values used when the selected method needs missing inputs

Important helper functions:

- `_serialize_history(history)`
  - Formats float values to 8 decimal places before rendering
- `_figure_to_base64(fig)`
  - Saves a matplotlib figure to an in-memory PNG
- `_build_plot_data(f, result, method)`
  - Calls `build_figure()` and returns an embeddable image string
- `_solve_request(form_data)`
  - Main orchestration function for solving a submitted equation

### `methods/`

Each method module returns a dictionary with a shared shape:

```python
{
    "root": float | None,
    "iterations": int,
    "errors": list[float],
    "history": list[dict],
    "converged": bool,
    "message": str
}
```

Implemented methods:

- `bisection.py`
  - Requires `a` and `b`
  - Uses interval halving
  - Returns failure when `f(a)` and `f(b)` do not have opposite signs
- `false_position.py`
  - Requires `a` and `b`
  - Uses linear interpolation inside the bracketed interval
- `newton.py`
  - Requires derivative `df` and initial guess `x0`
  - Stops if the derivative is too close to zero
- `secant.py`
  - Requires `x0` and `x1`
  - Approximates derivative from two recent points
- `mullers.py`
  - Requires `x0`, `x1`, and `x2`
  - Uses a quadratic fit through three points
  - Stops early if a complex discriminant appears
- `fixed_point.py`
  - Requires iteration function `g(x)` and initial guess `x0`
  - Tracks `x_{n+1} - x_n` as the error measure

### `utils/parser.py`

Responsibilities:

- Cleans the equation string
- Replaces `^` with `**`
- Validates the expression with a restricted evaluation namespace
- Builds a callable function `f(x)`
- Builds a derivative function `df(x)`

Derivative strategy:

- Uses SymPy symbolic differentiation when available
- Falls back to central-difference numerical differentiation with `h = 1e-7`

Supported expression space includes:

- arithmetic operators
- trigonometric functions
- hyperbolic functions
- exponentials and logarithms
- roots, powers, and absolute-value helpers
- constants such as `pi`, `e`, `tau`, and `inf`

Security note:

- The parser removes `__builtins__` and uses a curated namespace, which is safer than unrestricted `eval`.
- This is still not equivalent to a hardened sandbox and should be treated as controlled project input handling, not full isolation.

### `utils/graph.py`

Responsibilities:

- Configures matplotlib for server-side rendering with the `Agg` backend
- Generates a two-row figure:
  - function plot with root marker
  - convergence plot on a logarithmic y-scale
- Chooses a plotting window centered around the root or interval
- Filters invalid or extremely large values to avoid noisy plots

Implementation notes:

- Bisection shades the initial interval on the function plot
- The plotting theme uses a dark palette regardless of page theme
- Figures are returned as `matplotlib.figure.Figure` objects

### `utils/results.py`

Responsibilities:

- Save result data to CSV
- Load a subset of saved result data from CSV

Current integration status:

- Present in the repository
- Not currently used by the Flask route or the browser export button
- The browser export in `templates/index.html` creates a lightweight CSV on the client side instead

## Frontend Layer

### `templates/index.html`

Main UI sections:

- sticky navigation and theme toggle
- hero section with method badges
- control panel with equation, method selection, and parameter inputs
- results panel with status, summary metrics, plot, and iteration history

Client-side behaviors:

- switches visible parameter inputs based on selected method
- fills the equation field from example selections
- stores theme preference in `localStorage`
- exports a summary CSV in the browser

Important implementation detail:

- Method-specific fields are rendered from `METHOD_INFO`
- The template expects `result.history` to already be formatted for display

### `static/style.css`

The stylesheet provides:

- responsive two-column layout on desktop
- single-column layout on smaller screens
- light and dark theme variables
- card, table, button, and status-state styling

## Method Input Mapping

```text
Bisection       -> equation, a, b, tol, max_iter
False Position  -> equation, a, b, tol, max_iter
Newton-Raphson  -> equation, x0, tol, max_iter
Secant          -> equation, x0, x1, tol, max_iter
Muller's        -> equation, x0, x1, x2, tol, max_iter
Fixed Point     -> equation, x0, g(x), tol, max_iter
```

## Mathematical Formulas

This section lists the core update formulas used by each implemented root-finding method:

- **Bisection method**: given a bracket [a_n, b_n] with f(a_n)f(b_n) < 0, the next iterate is

  $x_{n+1} = (a_n + b_n) / 2$

  Update the bracket by replacing the endpoint with the same sign as f(x_{n+1}). Error bound after n iterations: |b_n - a_n| / 2.

- **False Position (Regula Falsi)**: linear interpolation inside [a_n, b_n]:

  $x_{n+1} = b_n - f(b_n) * (b_n - a_n) / (f(b_n) - f(a_n))$

- **Newton–Raphson**: uses the derivative f':

  $x_{n+1} = x_n - f(x_n) / f'(x_n)$

- **Secant method**: approximates the derivative from two recent points:

  $x_{n+1} = x_n - f(x_n) * (x_n - x_{n-1}) / (f(x_n) - f(x_{n-1}))$

- **Muller's method**: fit a quadratic p(x)=ax^2+bx+c through three points and take the root of the quadratic nearest x_n:

  $x_{n+1} = x_n + (-2c) / (b \pm sqrt(b^2 - 4ac))$

  (Choose the sign in the denominator to avoid cancellation — typical implementations select the sign of b that gives a larger-magnitude denominator.)

- **Fixed-point iteration**: iterate $x_{n+1} = g(x_n)$. Convergence at root r requires |g'(r)| < 1.

Notes on convergence orders: bisection is linear, Newton's method is typically quadratic, the secant method has order about phi ≈ 1.618, and false position often behaves like a linear method but may show superlinear behavior depending on the function.

## Known Technical Gaps

- `main.py` runs with Flask debug mode enabled.
- The frontend renders the `g` input for Fixed Point as `type="number"`, even though the backend expects an expression string. This is a UI/backend mismatch worth fixing.
- `utils/results.py` is partially disconnected from the current web workflow.
- There is no automated test coverage for route handling, parser validation, or solver correctness.
- Several source files still contain encoding artifacts in strings copied from older edits.

## Suggested Engineering Next Steps

1. Add unit tests for each numerical method and for `parse_equation()`.
2. Add Flask route tests for valid submissions and common validation failures.
3. Fix the Fixed Point `g(x)` input type in the template.
4. Replace the client-side export helper with server-generated CSV using `utils/results.py`.
5. Normalize file encodings to UTF-8 and clean up display text artifacts.

e-6, 100)
   print(result)
   ```

---

## Code Standards

- **Format**: PEP 8 (with line length ~100)
- **Documentation**: Docstrings for all functions
- **Naming**: snake_case for functions, UPPER_CASE for constants
- **Error Handling**: Try/except for user input, return errors gracefully
- **Comments**: Explain *why*, not *what* (code explains what)

---

*For usage guide, see FEATURES.md and README.md*
e-6, 100)
   print(result)
   ```

---

## Code Standards

- **Format**: PEP 8 (with line length ~100)
- **Documentation**: Docstrings for all functions
- **Naming**: snake_case for functions, UPPER_CASE for constants
- **Error Handling**: Try/except for user input, return errors gracefully
- **Comments**: Explain *why*, not *what* (code explains what)

---

*For usage guide, see FEATURES.md and README.md*
e-6, 100)
   print(result)
   ```

---

## Code Standards

- **Format**: PEP 8 (with line length ~100)
- **Documentation**: Docstrings for all functions
- **Naming**: snake_case for functions, UPPER_CASE for constants
- **Error Handling**: Try/except for user input, return errors gracefully
- **Comments**: Explain *why*, not *what* (code explains what)

---

*For usage guide, see FEATURES.md and README.md*
