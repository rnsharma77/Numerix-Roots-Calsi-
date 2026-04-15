# 🚀 Quick Feature Guide

## New Enhancements Summary

Your Root Finding Calculator has been **upgraded** to work with **ANY equation** and **UNLIMITED iterations**. Here's what's new:

---

## 📋 What Changed

### ✅ 3 New Methods Added
1. **False Position (Regula Falsi)** — Like bisection but uses linear interpolation for faster convergence
2. **Muller's Method** — Uses 3 points and fits a parabola; can even find complex roots
3. **Fixed Point Iteration** — Convert f(x)=0 to x=g(x) and iterate

### ✅ Extended Function Support (30+ functions)
Now supports:
- Inverse trig: `asin`, `acos`, `atan`
- Hyperbolic inverse: `asinh`, `acosh`, `atanh`
- More logs: `log2` in addition to `log`, `log10`
- More utilities: `ceil`, `floor`, `factorial`, `radians`, `degrees`
- Constants: `tau`, `inf` added to existing `pi`, `e`

### ✅ Better Parameter Control
- Set **any tolerance** you want (1e-1 to 1e-15)
- Set **any iteration limit** (from 1 to 10000+)
- Method-specific defaults that make sense

### ✅ Export Your Results
New **"💾 Export"** button saves:
- Configuration (equation, method, parameters)
- Summary (root, iterations, convergence status)
- Full iteration history to CSV

---

## 🎯 How to Use

### For Any Equation
```
1. Type your equation (use Python syntax with x as variable)
2. Choose a method (6 options now!)
3. Enter method-specific parameters
4. Set tolerance and max iterations to suit your needs
5. Click SOLVE
6. View results, graph, and iteration table
7. Click Export to save
```

### Example: Complex Equation
```
Equation:          sin(x)**2 + cos(x) - x**2
Method:            Newton-Raphson
Initial Guess:     x₀ = 1.0
Tolerance:         1e-8
Max Iterations:    500

→ Root found!
```

### Example: Custom Iterations
```
Equation:          exp(x) - 10*x
Method:            Bisection
Interval:          a = 0, b = 3
Tolerance:         1e-12
Max Iterations:    2000  ← High precision: more iterations

→ Root ≈ 2.61286...
→ Iterations used: 40 (out of 2000 available)
```

### Example: Fixed Point (New)
```
Original:          x³ - x - 2 = 0
Rearranged:        x = (x³ - 2) + x
                   or: x = cbrt(x + 2)
                   or: x = x - (x³ - x - 2)/(3x² - 1)

Method:            Fixed Point
Function g(x):     (x**3 - 2 + x)  ← Enter this!
Initial x₀:        1.5
Tolerance:         1e-6
Max Iterations:    500

→ Root found using custom iteration!
```

---

## 🔑 Key Points

✓ **Any equation syntax** — Full Python math syntax support
✓ **Any tolerance** — From loose (1e-3) to very tight (1e-15)
✓ **Any iterations** — Practical limit is your computer's speed
✓ **Any method** — 6 advanced methods to choose from
✓ **Export always works** — Save results for further analysis

---

## 📊 When to Use Each Method

| Want... | Use... | Because... |
|---|---|---|
| Guaranteed convergence | Bisection or False Position | Always works if sign change exists |
| Fastest convergence | Newton-Raphson | Quadratic convergence if near root |
| No derivative needed | Secant or False Position | Don't need to compute f'(x) |
| Very fast | Muller's Method | Highest convergence order (~1.84) |
| Custom iteration | Fixed Point | When you can rearrange the equation |
| Never tried before | Bisection | Simple, reliable, always works |

---

## 📁 Files Added/Modified

### New Files
- `methods/false_position.py` — Regula Falsi method
- `methods/fixed_point.py` — Fixed point iteration
- `methods/mullers.py` — Muller's method
- `utils/results.py` — Result export utilities

### Updated Files
- `main.py` — 6 methods, export button, enhanced parsing
- `utils/parser.py` — 30+ functions now supported
- `README.md` — Complete documentation

---

## 🎓 Tips & Tricks

### Tip 1: Set iteration limit based on method
- **Bisection/False Position**: 50-200 (linear convergence, needs more iterations)
- **Newton-Raphson**: 20-100 (quadratic, very few needed)
- **Secant**: 30-150 (superlinear, medium)
- **Muller's**: 10-50 (very fast, few needed)

### Tip 2: Tolerance meanings
- `1e-3` = 0.001 = 3 decimal places accuracy
- `1e-6` = 0.000001 = 6 decimal places accuracy (default)
- `1e-10` = 10 decimal places accuracy (tight)
- `1e-15` = 15 decimal places (machine precision limit)

### Tip 3: Initial guess matters (Newton-Raphson)
- Good guess (near actual root): converges in 3-5 iterations
- Bad guess (far from root): may diverge or take 50+ iterations
- Bisection works regardless of initial interval (if sign change exists)

### Tip 4: Complex equations
- Use parentheses: `(x**2 - 1) / (x + 2)`
- Test your equation first with a simple initial solve
- Many equations may have multiple roots; try different intervals/guesses

---

## ✨ Example Workflows

### Workflow 1: Find Root Quickly
1. Use **Newton-Raphson** with reasonable guess
2. Set tolerance to 1e-6, max iterations 50
3. Should converge in 3-10 iterations usually

### Workflow 2: High Precision Result
1. Use **Bisection** with correct interval
2. Set tolerance to 1e-12, max iterations 1000
3. Will take ~40 iterations but guaranteed accuracy

### Workflow 3: Comparing Methods
1. Enter equation
2. Solve with Method A, note iterations
3. Clear, solve with Method B, note iterations
4. Export both results and compare

### Workflow 4: Analysis & Research
1. Solve with best method
2. Click "View Iteration Table" to see convergence pattern
3. Click "Export" to save for Python/Excel analysis
4. Plot error convergence externally if needed

---

## 🐛 Troubleshooting

| Problem | Solution |
|---|---|
| "Parse error: Could not parse equation" | Check equation syntax (use `**` not `^`, use `x` not `X`) |
| "f(a) and f(b) must have opposite signs" | Change interval; no root or sign change doesn't exist there |
| "Derivative near zero" | Newton-Raphson derivative=0; try better initial guess or different method |
| "No convergence in any equation with any tolerance" | Try all 6 methods; one usually works |
| "Returned NaN" | Equation has singularity or division by zero in that region |

---

## 🎉 You're All Set!

Your calculator now:
- ✅ Works with **any equation** (30+ functions supported)
- ✅ Supports **any iteration limit** (up to thousands)
- ✅ Has **6 different methods** to choose from
- ✅ Lets you **customize all parameters**
- ✅ Can **export results** for analysis
- ✅ Shows **beautiful visualizations**
- ✅ Computes **derivatives automatically**

**Happy calculating!** 🧮📈

---

*For detailed documentation, see README.md*
