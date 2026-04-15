"""
Graph utility: plots function curve, root marker, and convergence error graph.
Returns matplotlib Figure objects that can be saved or embedded in a web page.
"""

import numpy as np
import matplotlib
matplotlib.use("Agg")
from matplotlib.figure import Figure
import matplotlib.gridspec as gridspec


# ── Palette ────────────────────────────────────────────────────────────────
PALETTE = {
    "bg":       "#0D1117",
    "panel":    "#161B22",
    "accent":   "#00FFA3",
    "accent2":  "#FF6B6B",
    "accent3":  "#FFD93D",
    "grid":     "#21262D",
    "text":     "#E6EDF3",
    "muted":    "#8B949E",
    "curve":    "#58A6FF",
    "zero":     "#3D444D",
}


def apply_dark_style(ax, bg=PALETTE["bg"], panel=PALETTE["panel"]):
    ax.set_facecolor(panel)
    ax.tick_params(colors=PALETTE["muted"], labelsize=8)
    ax.xaxis.label.set_color(PALETTE["muted"])
    ax.yaxis.label.set_color(PALETTE["muted"])
    ax.title.set_color(PALETTE["text"])
    for spine in ax.spines.values():
        spine.set_edgecolor(PALETTE["grid"])
    ax.grid(True, color=PALETTE["grid"], linestyle="--", linewidth=0.5, alpha=0.7)


def build_figure(f, root, errors, method_name, a=None, b=None):
    """
    Build a matplotlib Figure with two subplots:
      1. Function curve + root marker
      2. Convergence (error per iteration, log scale)

    Returns a Figure instance.
    """
    fig = Figure(figsize=(9, 6), facecolor=PALETTE["bg"])
    gs = gridspec.GridSpec(2, 1, figure=fig, hspace=0.45,
                           top=0.92, bottom=0.10, left=0.10, right=0.97)

    # ── 1. Function Plot ───────────────────────────────────────────────────
    ax1 = fig.add_subplot(gs[0])
    apply_dark_style(ax1)

    # Determine x range
    if root is not None:
        center = root
    elif a is not None and b is not None:
        center = (a + b) / 2
    else:
        center = 1.0

    span = max(abs(a - b) * 2 if (a is not None and b is not None) else 6, 6)
    x_min = center - span / 2
    x_max = center + span / 2

    xs = np.linspace(x_min, x_max, 800)
    ys = []
    for xi in xs:
        try:
            yi = f(xi)
            if abs(yi) > 1e10:
                yi = np.nan
        except Exception:
            yi = np.nan
        ys.append(yi)
    ys = np.array(ys)

    ax1.plot(xs, ys, color=PALETTE["curve"], linewidth=2.0, label="f(x)", zorder=3)
    ax1.axhline(0, color=PALETTE["zero"], linewidth=1.2, zorder=2)
    ax1.axvline(0, color=PALETTE["zero"], linewidth=0.8, zorder=2)

    if root is not None:
        try:
            fy = f(root)
            ax1.scatter([root], [fy], color=PALETTE["accent"],
                        s=120, zorder=5, label=f"Root ≈ {root:.6f}", edgecolors="white", linewidths=0.8)
            ax1.axvline(root, color=PALETTE["accent"], linewidth=1.0,
                        linestyle="--", alpha=0.5, zorder=4)
        except Exception:
            pass

    # Shade interval for bisection
    if a is not None and b is not None and method_name == "Bisection":
        ax1.axvspan(a, b, alpha=0.07, color=PALETTE["accent3"])

    ax1.set_title(f"Function Plot  ·  {method_name} Method",
                  fontsize=10, fontweight="bold", pad=8)
    ax1.set_xlabel("x", fontsize=9)
    ax1.set_ylabel("f(x)", fontsize=9)
    handles1, labels1 = ax1.get_legend_handles_labels()
    if labels1:
        ax1.legend(fontsize=8, facecolor=PALETTE["panel"],
                   labelcolor=PALETTE["text"], edgecolor=PALETTE["grid"])

    # ── 2. Convergence Plot ────────────────────────────────────────────────
    ax2 = fig.add_subplot(gs[1])
    apply_dark_style(ax2)

    if errors and len(errors) > 0:
        iters = list(range(1, len(errors) + 1))
        ax2.semilogy(iters, errors, color=PALETTE["accent2"],
                     linewidth=1.8, marker="o", markersize=3.5,
                     markerfacecolor=PALETTE["accent3"], zorder=3, label="Error")
        ax2.fill_between(iters, errors, alpha=0.12, color=PALETTE["accent2"])
    else:
        ax2.text(0.5, 0.5, "No convergence data", transform=ax2.transAxes,
                 ha="center", va="center", color=PALETTE["muted"], fontsize=9)

    ax2.set_title("Convergence  ·  Error vs Iteration", fontsize=10, fontweight="bold", pad=8)
    ax2.set_xlabel("Iteration", fontsize=9)
    ax2.set_ylabel("Absolute Error (log)", fontsize=9)
    handles2, labels2 = ax2.get_legend_handles_labels()
    if labels2:
        ax2.legend(fontsize=8, facecolor=PALETTE["panel"],
                   labelcolor=PALETTE["text"], edgecolor=PALETTE["grid"])

    return fig
