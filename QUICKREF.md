# ⚡ Quick Reference Card

## 🚀 Getting Started (30 seconds)

```bash
pip install -r requirements.txt
python main.py
```

## 🎯 The 6 Methods

| # | Method | Best For | Inputs | Speed |
|---|--------|----------|--------|-------|
| 1 | **Bisection** | Guaranteed root finding | Interval [a, b] | ⭐⭐ |
| 2 | **False Position** | Faster bisection | Interval [a, b] | ⭐⭐⭐ |
| 3 | **Newton-Raphson** | Speed priority | Guess x₀ | ⭐⭐⭐⭐⭐ |
| 4 | **Secant** | No derivative needed | x₀, x₁ | ⭐⭐⭐⭐ |
| 5 | **Muller's** | Very fast convergence | x₀, x₁, x₂ | ⭐⭐⭐⭐⭐ |
| 6 | **Fixed Point** | Custom iteration | x₀, g(x) | ⭐⭐⭐ |

## 📝 Common Equations

```
Cubic              x**3 - x - 2
Transcendental     cos(x) - x
Exponential        exp(x) - 3*x
Trigonometric      sin(x) - x/2
Logarithmic        log(x) - 1
Radical            sqrt(x) - 2
Rational           x - 1/x
Mixed              sin(x)**2 + cos(x) - x**2
```

## 🔑 Parameters Explained

| Parameter | Purpose | Default | Range |
|-----------|---------|---------|-------|
| **Tolerance** | Stop when error < this | 1e-6 | 1e-1 to 1e-15 |
| **Max Iters** | Stop when iterations > this | 100 | 1 to 10000+ |
| **x₀ (guess)** | Starting point | 1.5 | Any real number |
| **a, b (interval)** | Bracket for root | 1, 2 | a < b, opposite signs |

## ⚙️ 30+ Functions Reference

### Trig & Inverse
`sin(x)`, `cos(x)`, `tan(x)`, `asin(x)`, `acos(x)`, `atan(x)`

### Hyperbolic & Inverse
`sinh(x)`, `cosh(x)`, `tanh(x)`, `asinh(x)`, `acosh(x)`, `atanh(x)`

### Logarithmic & Exponential
`log(x)` (ln), `log10(x)`, `log2(x)`, `exp(x)`

### Power & Root
`sqrt(x)`, `pow(x, n)`, `x**n`

### Utilities
`abs(x)`, `ceil(x)`, `floor(x)`, `factorial(x)`, `min(a, b)`, `max(a, b)`

### Angle Conversion
`degrees(x)`, `radians(x)`

### Constants
`pi`, `e`, `tau` (2π), `inf`

## 🎓 When to Use Each Method

### ✅ Always Try First
→ **Bisection** if you know the interval and signs differ at endpoints

### ✅ For Speed
→ **Newton-Raphson** if you can provide good initial guess

### ✅ When Stuck
→ Cycle through all 6 methods, one will work

### ✅ For Analysis
→ **False Position** to compare with Bisection
→ **Muller's** for comparison with Newton

### ✅ For Custom
→ **Fixed Point** when you can rearrange equation creatively

## 💡 Pro Tips

### Tip 1: Choosing Tolerance
- `1e-3` = 3 decimal places (loose)
- `1e-6` = 6 decimal places (standard, default)
- `1e-10` = 10 decimal places (tight)
- `1e-15` = 15 decimal places (machine limit)

### Tip 2: Iteration Defaults
- **Bisection/FalsePos**: 50-500 (linear, needs more)
- **Newton**: 10-50 (quadratic, very few)
- **Secant**: 20-100 (superlinear, medium)
- **Muller's**: 5-50 (very fast)

### Tip 3: Initial Guess
- **Newton**: Must be CLOSE to root or it diverges
- **Secant**: Two guesses bracket or nearby
- **Bisection**: Doesn't matter if signs differ

### Tip 4: Testing Equation
Before solving, make sure syntax is valid:
```python
# In Python terminal:
from utils.parser import parse_equation
f, df, _, err = parse_equation("x**2 - 4")
print(f(2))   # Should be ~0
print(f(3))   # Should be ~5
```

## 📊 Typical Convergence

| Method | Typical Iterations for 1e-6 |
|--------|-----|
| Bisection | 20 |
| False Position | 5-15 |
| Newton-Raphson | 3-8 |
| Secant | 8-15 |
| Muller's | 4-8 |

*Actual depends on equation and initial guess*

## 🔧 Troubleshooting (Quick)

| Problem | Try This |
|---------|----------|
| "Parse error" | Check `**` (not `^`), use lowercase `x` |
| "Opposite signs" | Change interval a, b |
| "Zero derivative" | Better initial guess for Newton |
| "Not converging" | Increase Max Iterations |
| "Wrong root" | Different initial guess/interval |

## 📤 Export Results

After solving:
1. Click **"💾 Export"** button
2. Choose save location
3. Opens CSV with:
   - Equation & method used
   - Root found and convergence info
   - Complete iteration table

## 🎬 Workflow Examples

### Quick Check (2 seconds)
```
1. Enter equation
2. Click SOLVE (Bisection is default)
3. See root immediately
```

### Detailed Analysis (1 minute)
```
1. Enter equation
2. Try different initial guesses with Newton
3. Click table button to see iteration details
4. Export results
```

### Comparison Study (5 minutes)
```
1. Bisection: note iterations
2. Newton-Raphson: compare iterations
3. Muller's: compare iterations
4. Export all 3 results
```

## 🎯 Success Indicators

✅ **Green text** in results = Converged (good!)
✅ **Yellow/Red text** = Did not converge (try different method/params)
✅ **Graph shows root** on x-axis at zero crossing = Correct!
✅ **Error decreasing** in bottom graph = Converging well!

## 🚨 Error Messages & Fixes

| Message | Meaning | Fix |
|---------|---------|-----|
| "Could not parse" | Syntax error | Fix equation |
| "Opposite signs required" | No bracket | New interval a, b |
| "Division by zero" | f'(x)=0 | Different guess |
| "Max iterations" | Too slow | Increase max iters |
| "NaN returned" | Invalid domain | Avoid domain gaps |

## 📚 Learn More

- **FEATURES.md** - Full feature guide
- **README.md** - Complete documentation
- **TECHNICAL.md** - How methods work internally

---

**Remember:** When in doubt, try **Bisection** first — it always works! 🎯
