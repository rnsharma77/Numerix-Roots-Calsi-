# 🔧 Technical Documentation

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                          main.py (GUI)                          │
│  - RootFinderApp(tk.Tk): Main window and layout                 │
│  - IterationTableDialog: Results table view                      │
│  - StyledEntry, StyledButton: Custom widgets                    │
└──────────────────┬──────────────────────┬──────────────────────┘
                   │                      │
        ┌──────────▼────────────┐  ┌─────▼──────────────────┐
        │  methods/ package     │  │  utils/ package        │
        ├───────────────────────┤  ├────────────────────────┤
        │ • bisection.py        │  │ • parser.py            │
        │ • newton.py           │  │ • graph.py             │
        │ • secant.py           │  │ • results.py (NEW)     │
        │ • false_position.py   │  │                        │
        │ • mullers.py          │  │ Parsing: str → callable
        │ • fixed_point.py      │  │ Graphs: f, errors → Fig
        └───────────────────────┘  │ Export: results → CSV  │
                                    └────────────────────────┘
```

---

## Module Descriptions

### `main.py` (527 lines)
**Purpose**: GUI application entry point using Tkinter

**Key Classes**:
- `RootFinderApp(tk.Tk)` — Main application window
  - `_build_ui()` — Construct UI layout
  - `_build_left_panel()` — Left sidebar (controls)
  - `_build_inputs()` — Dynamic method-specific inputs
  - `_solve()` — Execute selected method
  - `_display_results()` — Show solution in UI
  - `_plot()` — Render graph
  - `_export_results()` — Save to CSV

- `IterationTableDialog(tk.Toplevel)` — Shows iteration details

- `StyledEntry`, `StyledButton`, `SectionLabel` — Custom widgets

- `Tooltip` — Hover help text

**Flow**:
1. User enters equation + parameters
2. Click SOLVE → `_solve()` method
3. Parse equation → `parse_equation()`
4. Call method (bisection, newton, etc.)
5. Display results → `_display_results()`
6. Render graph → `_plot()` via matplotlib

---

### `methods/` Package

#### `bisection.py`
```python
def bisection(f, a, b, tol=1e-6, max_iter=100) -> dict
```
- **Inputs**: Continuous function f on [a,b] with f(a)·f(b) < 0
- **Algorithm**: Recursive interval halving
- **Returns**: `{root, iterations, errors, history, converged, message}`
- **Time**: O(log(1/tol)) evaluations
- **Guaranteed**: Always converges if sign change exists

#### `false_position.py` (NEW)
```python
def false_position(f, a, b, tol=1e-6, max_iter=100) -> dict
```
- **Improvement**: Uses linear interpolation instead of midpoint
- **Formula**: c = (a·f(b) - b·f(a)) / (f(b) - f(a))
- **Faster**: Converges faster than bisection typically
- **Guaranteed**: Like bisection, always works with sign change

#### `newton.py`
```python
def newton_raphson(f, df, x0, tol=1e-6, max_iter=100) -> dict
```
- **Requires**: f(x) and f'(x)
- **Formula**: x_{n+1} = x_n - f(x_n)/f'(x_n)
- **Speed**: Quadratic convergence (very fast!)
- **Risks**: Can diverge with bad x0 or if f'(x) ≈ 0

#### `secant.py`
```python
def secant(f, x0, x1, tol=1e-6, max_iter=100) -> dict
```
- **No derivative needed** — Approximates f'(x) numerically
- **Formula**: x_{n+1} = x_n - f(x_n)·(x_n - x_{n-1})/(f(x_n) - f(x_{n-1}))
- **Speed**: Superlinear (order ≈ 1.618)
- **Uses**: Two initial guesses, not one

#### `mullers.py` (NEW)
```python
def mullers_method(f, x0, x1, x2, tol=1e-6, max_iter=100) -> dict
```
- **Inputs**: Three initial guesses
- **Algorithm**: Fits parabola through 3 points
- **Speed**: Very fast (order ≈ 1.84)
- **Unique**: Can find complex roots (returns real when available)

#### `fixed_point.py` (NEW)
```python
def fixed_point(g, x0, tol=1e-6, max_iter=100) -> dict
```
- **Setup**: User provides rearrangement g such that x = g(x)
- **Formula**: x_{n+1} = g(x_n)
- **Convergence**: Depends on |g'(x*)| where x* is fixed point
- **Flexible**: User controls iteration function

**Result Dictionary Structure**:
```python
{
    "root": float,           # The found root
    "iterations": int,       # Iterations performed
    "errors": [float, ...],  # Error per iteration
    "history": [dict, ...],  # Detailed iteration data
    "converged": bool,       # Convergence status
    "message": str          # Status message
}
```

---

### `utils/parser.py`
**Purpose**: Convert equation string to callable function + derivative

**Function**:
```python
def parse_equation(expr_str: str) -> (callable, callable, str, str|None)
```

**Returns**:
- `f(x)` — Function evaluator
- `df(x)` — Derivative (symbolic via SymPy, else numerical)
- `expr_str` — Cleaned equation string
- `error` — Error message if parsing failed

**Supported**:
- All Python math operators: `+`, `-`, `*`, `/`, `**`, `()`, etc.
- 30+ functions: trig, hyperbolic, exponential, logarithmic, power, utilities
- Constants: `pi`, `e`, `tau`, `inf`

**Security**:
- Uses restricted namespace (`__builtins__` removed)
- Prevents arbitrary code execution

**Derivatives**:
1. **SymPy**: Symbolic differentiation if available
2. **Fallback**: Central difference numerical derivative (h=1e-7)

---

### `utils/graph.py`
**Purpose**: Generate matplotlib Figure with function plot + convergence graph

**Function**:
```python
def build_figure(f, root, errors, method_name, a=None, b=None) -> Figure
```

**Output**: 2-subplot figure
- **Top**: Function curve + root marker + interval (for bisection)
- **Bottom**: Convergence analysis (error vs iteration, log scale)

**Features**:
- Dark theme (GitHub-inspired)
- Automatic range detection
- Handles singularities (NaN removal)
- Color-coded elements
- Grid, labels, legend

---

### `utils/results.py` (NEW)
**Purpose**: Save/load analysis results

**Functions**:
```python
def save_results_to_csv(file_path, equation, method, result, tolerance, max_iterations) -> bool

def load_results_from_csv(file_path) -> dict|None
```

**CSV Format**:
```csv
Root Finding Calculator - Results,
Generated,2024-11-28 10:30:45

Configuration:
Equation,x**3 - x - 2
Method,Newton-Raphson
Tolerance,1e-06
Max Iterations,100

Results Summary:
Root Found,1.521379706800...
Iterations Performed,5
Converged,Yes
Final Error,5.32e-13
Message,Converged in 5 iterations. Root ≈ 1.52137970680000

Iteration History:
iter,root,f_root,error,x_prev
1,1.365...,0.1234...,0.135...,1.5
2,1.521...,0.0012...,0.156...,1.365...
...
```

---

## Data Flow

### Solving an Equation (Example: Newton-Raphson)

```
1. User clicks SOLVE
   ↓
2. main.py._solve() executes
   ├─ Parse equation string → f(x), f'(x)
   ├─ Read tolerance & max_iter
   ├─ Read method parameters (x0)
   ├─ Call newton.newton_raphson(f, df, x0, tol, max_iter)
   └─ Result dict returned
   ↓
3. _display_results() shows:
   ├─ Root value (in green if convergence)
   ├─ Iteration count
   ├─ Final error
   └─ Status message
   ↓
4. _plot() generates graph:
   ├─ plot_function + root marker
   ├─ convergence_error log plot
   └─ Render in Tkinter canvas
   ↓
5. User can:
   ├─ View "iteration Table" → IterationTableDialog
   ├─ Click "Export" → save CSV
   └─ Solve new equation
```

---

## Adding a New Method

### Step 1: Create method file
```python
# methods/new_method.py

def new_method(f, param1, param2, tol=1e-6, max_iter=100):
    """
    Find root using [Method Name].
    
    Returns:
        dict with keys: root, iterations, errors, history, converged, message
    """
    errors = []
    history = []
    
    for i in range(1, max_iter + 1):
        # Your algorithm here
        x_new = compute_next_x(...)
        error = abs(x_new - x_prev)
        
        errors.append(error)
        history.append({
            "iter": i,
            "root": x_new,
            "f_root": f(x_new),
            "error": error,
            # ... other details
        })
        
        if error < tol:
            return {
                "root": x_new,
                "iterations": i,
                "errors": errors,
                "history": history,
                "converged": True,
                "message": f"Converged in {i} iterations."
            }
    
    return {
        "root": x_new,
        "iterations": max_iter,
        "errors": errors,
        "history": history,
        "converged": False,
        "message": f"Max iterations reached."
    }
```

### Step 2: Import in main.py
```python
from methods.new_method import new_method
```

### Step 3: Add to METHOD_INFO
```python
METHOD_INFO = {
    ...
    "New Method": {"inputs": ["param1", "param2"], "keys": ["p1", "p2"]},
}
```

### Step 4: Add to _solve() switch
```python
elif method == "New Method":
    result = new_method(f, inputs["p1"], inputs["p2"], tol, max_iter)
    result["_a"], result["_b"] = None, None
```

Done! New method now available in dropdown.

---

## Supported Output Formats

### Current: CSV via `_export_results()`

### Future: Could add
- **JSON** for structured data
- **PDF** with formatted report
- **Excel** with formulas
- **LaTeX** for academic papers
- **HTML** with interactive plots

---

## Performance Characteristics

| Method | Time per iteration | Total for 1e-6 accuracy |
|---|---|---|
| Bisection | O(1) | ~20 iterations |
| False Position | O(1) | ~8-15 iterations |
| Newton-Raphson | O(1) + f'(x) | 3-10 iterations |
| Secant | O(1) | 8-15 iterations |
| Muller's | O(1) | 4-8 iterations |
| Fixed Point | O(1) + g(x) | 10-100+ iterations |

**Notes**:
- Actual iterations depend on:
  - Equation difficulty (smoothness, root multiplicity)
  - Method implementation details
  - Initial guess quality
  - Convergence tol tolerance

---

## Testing Equations

### Simple Tests
```python
# Linear: x = 1 (obvious, all methods converge instantly)
"x - 1"

# Quadratic: x = ±2
"x**2 - 4"

# Cubic: x ≈ 1.52
"x**3 - x - 2"
```

### Medium Tests
```python
"cos(x) - x"           # Transcendental mix
"exp(x) - 3*x"         # Exponential growth vs. linear
"sin(x)/x - 0.5"       # Oscillation + division
```

### Hard Tests
```python
"x**10 - 1"            # High power (multiple roots)
"tan(x) - x"           # Singularities (asymptotes)
"exp(-x**2) - 0.5"     # Flat near center
```

---

## Debugging Tips

### If method doesn't converge:
1. Check equation syntax in terminal:
   ```python
   from utils.parser import parse_equation
   f, df, eq, err = parse_equation("your_equation")
   print(f(1.0), df(1.0))  # Should return numbers
   ```

2. Visualize equation (external):
   ```python
   import numpy as np
   import matplotlib.pyplot as plt
   x = np.linspace(-5, 5, 1000)
   y = [f(xi) for xi in x]
   plt.plot(x, y)
   plt.grid()
   plt.show()
   ```

3. Test specific method manually:
   ```python
   from methods.newton import newton_raphson
   result = newton_raphson(f, df, 1.5, 1e-6, 100)
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
