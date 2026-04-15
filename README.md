# Root Finding Calculator

A Flask-based web application for solving nonlinear equations with classical numerical methods. The project combines a browser UI, Python solver modules, equation parsing, and matplotlib-based visualizations in a single lightweight app.

## Project Analysis

This repository is organized as a small full-stack Python app:

- `main.py` runs the Flask server, validates form input, dispatches each numerical method, and prepares results for the template.
- `methods/` contains the root-finding implementations.
- `utils/parser.py` turns user-entered expressions into callable functions and derivatives.
- `utils/graph.py` generates the function plot and convergence plot.
- `templates/index.html` renders the UI, result summary, plot, and iteration table.
- `static/style.css` contains the responsive styling and theme support.
- `utils/results.py` provides CSV save/load helpers, though the current web UI exports a smaller CSV directly in the browser.

## Supported Methods

- Bisection
- False Position
- Newton-Raphson
- Secant
- Muller's Method
- Fixed Point Iteration

## Features

- Solve equations entered with Python-style math syntax such as `x**3 - x - 2`
- Support common functions like `sin`, `cos`, `tan`, `exp`, `log`, and `sqrt`
- Auto-generate symbolic derivatives with SymPy when possible
- Fall back to numerical differentiation when symbolic differentiation is unavailable
- Show convergence status, root estimate, iteration count, and final error
- Plot both the function curve and error-vs-iteration graph
- Display per-iteration history in a table
- Offer light and dark theme switching in the browser

## Requirements

- Python 3.10+ recommended
- Dependencies listed in `requirements.txt`

Install dependencies with:

```bash
pip install -r requirements.txt
```

## Running The App

From the `root-finding-calculator` folder:

```bash
python main.py
```

Then open:

```text
http://127.0.0.1:5000
```

## Equation Input Notes

- Use `x` as the variable.
- Use `**` for powers. The parser also converts `^` to `**`.
- Example inputs:
  - `x**3 - x - 2`
  - `cos(x) - x`
  - `exp(x) - 3*x`
  - `log(x) - 1`
  - `sqrt(x) - 2`

For Fixed Point Iteration, enter:

- the original equation in the equation field
- a separate iteration function `g(x)` in the method-specific input

## Project Structure

```text
root-finding-calculator/
|-- main.py
|-- requirements.txt
|-- README.md
|-- TECHNICAL.md
|-- methods/
|   |-- __init__.py
|   |-- bisection.py
|   |-- false_position.py
|   |-- fixed_point.py
|   |-- mullers.py
|   |-- newton.py
|   `-- secant.py
|-- utils/
|   |-- __init__.py
|   |-- graph.py
|   |-- parser.py
|   `-- results.py
|-- templates/
|   `-- index.html
`-- static/
    `-- style.css
```

## Current Behavior And Limitations

- The Flask app currently runs with `debug=True` in `main.py`.
- Solver methods return structured dictionaries with convergence status, history, and messages.
- Function parsing uses a restricted namespace, but expressions are still evaluated dynamically and should be treated as an academic-project feature rather than hardened sandboxing.
- The browser export button currently downloads summary data only; it does not use the richer CSV export helper in `utils/results.py`.
- There is no automated test suite in the repository yet.

## Recommended Next Improvements

- Add automated tests for parser behavior, solver correctness, and route handling
- Wire server-side CSV export to `utils/results.py`
- Add input validation in the frontend for method-specific fields
- Improve handling for method-specific edge cases and domain errors

