"""Generate the figures for the graphical proof (docs/figures/*.png).

Run:  python make_figures.py
"""
import os
import sys
import time

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))
from termboost.algorithms import binary_search, formula, count_up_to  # noqa: E402

FIG = os.path.join(os.path.dirname(__file__), "docs", "figures")
os.makedirs(FIG, exist_ok=True)


def valid(a, b, x):
    return (x % a == 0) ^ (x % b == 0)


# ---------------------------------------------------------------------------
def fig_number_line(a=3, b=5, upto=None):
    """Fig 1: the valid set is the merge of two arithmetic progressions."""
    upto = upto or 2 * a * b
    fig, ax = plt.subplots(figsize=(11, 2.8))
    xs = np.arange(1, upto + 1)
    ax.hlines(0, 0, upto + 1, color="#bbbbbb", lw=1, zorder=0)
    # multiples of a and b
    ma = [x for x in xs if x % a == 0]
    mb = [x for x in xs if x % b == 0]
    both = [x for x in xs if x % (a * b) == 0]
    ax.scatter(ma, [0.35] * len(ma), marker="v", color="#1f77b4", s=60,
               label=f"multiples of a={a}", zorder=3)
    ax.scatter(mb, [-0.35] * len(mb), marker="^", color="#ff7f0e", s=60,
               label=f"multiples of b={b}", zorder=3)
    # valid numbers on the line
    vs = [x for x in xs if valid(a, b, x)]
    ax.scatter(vs, [0] * len(vs), color="#2ca02c", s=90, zorder=4,
               label="valid (a xor b)")
    ax.scatter(both, [0] * len(both), facecolors="none", edgecolors="red",
               s=150, lw=2, zorder=5, label="excluded (a*b, both)")
    for k, x in enumerate(vs, start=1):
        ax.annotate(str(k), (x, 0.12), ha="center", fontsize=8, color="#2ca02c")
    ax.axvline(a * b, color="red", ls=":", lw=1)
    ax.text(a * b, 0.62, "period a·b", color="red", ha="center", fontsize=9)
    ax.set_title(f"Valid numbers = merge of two APs (a={a}, b={b}); "
                 f"{a + b - 2} per period", fontsize=11)
    ax.set_yticks([])
    ax.set_ylim(-0.8, 0.8)
    ax.legend(loc="lower right", fontsize=8, ncol=2)
    fig.tight_layout()
    fig.savefig(os.path.join(FIG, "fig1_number_line.png"), dpi=130)
    plt.close(fig)


# ---------------------------------------------------------------------------
def fig_period(a=3, b=5, periods=3):
    """Fig 2: periodicity - exactly p = a+b-2 valid numbers per period."""
    upto = periods * a * b
    fig, ax = plt.subplots(figsize=(11, 2.6))
    vs = [x for x in range(1, upto + 1) if valid(a, b, x)]
    colors = plt.cm.viridis(np.linspace(0, 0.85, periods))
    for k in range(periods):
        seg = [x for x in vs if k * a * b < x <= (k + 1) * a * b]
        ax.scatter(seg, [0] * len(seg), color=colors[k], s=70, zorder=3)
        ax.axvspan(k * a * b, (k + 1) * a * b, alpha=0.06, color=colors[k])
        ax.text((k + 0.5) * a * b, 0.5, f"{len(seg)} valid",
                ha="center", fontsize=10)
    for k in range(periods + 1):
        ax.axvline(k * a * b, color="#888", ls=":", lw=1)
    ax.set_title(f"Periodicity: p = a+b-2 = {a + b - 2} valid numbers in every "
                 f"block of length a·b = {a * b}", fontsize=11)
    ax.set_yticks([])
    ax.set_ylim(-0.6, 0.9)
    ax.set_xlabel("integer line")
    fig.tight_layout()
    fig.savefig(os.path.join(FIG, "fig2_period.png"), dpi=130)
    plt.close(fig)


# ---------------------------------------------------------------------------
def fig_staircase(a=7, b=11):
    """Fig 3: counting staircase C(v) vs the density line; V_r lands on it."""
    s = a + b
    p = a + b - 2
    xmax = a * b
    xs = np.arange(0, xmax + 1)
    C = [count_up_to(a, b, x) for x in xs]
    fig, ax = plt.subplots(figsize=(9, 6))
    ax.step(xs, C, where="post", color="#1f77b4", lw=1.6,
            label=r"$C(v)=\lfloor v/a\rfloor+\lfloor v/b\rfloor-2\lfloor v/ab\rfloor$")
    ax.plot(xs, xs * (1 / a + 1 / b), color="#d62728", ls="--", lw=1.4,
            label=r"density line $v\,(1/a+1/b)$")
    # mark a few r-th valid numbers found by the formula
    for r in range(1, p + 1, max(1, p // 8)):
        vr = formula(a, b, r)
        ax.scatter([vr], [r], color="#2ca02c", s=55, zorder=5)
        ax.annotate(f"r={r}", (vr, r), textcoords="offset points",
                    xytext=(5, -9), fontsize=8, color="#2ca02c")
    ax.set_title(f"r-th valid number $V_r\\approx r\\,ab/(a+b)$  (a={a}, b={b})",
                 fontsize=11)
    ax.set_xlabel("v")
    ax.set_ylabel("rank / count")
    ax.legend(fontsize=9)
    ax.grid(alpha=0.25)
    fig.tight_layout()
    fig.savefig(os.path.join(FIG, "fig3_staircase.png"), dpi=130)
    plt.close(fig)


# ---------------------------------------------------------------------------
def fig_invariant(a=7, b=11):
    """Fig 4: the key lemma i+j = r-1, and frac parts summing to 1."""
    s = a + b
    p = a + b - 2
    rs = np.arange(1, p + 1)
    i = (rs * b) // s
    j = (rs * a) // s
    frac_sum = (rs * b % s) / s + (rs * a % s) / s

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4.6))
    ax1.plot(rs, i + j, "o-", color="#1f77b4", label=r"$i+j$")
    ax1.plot(rs, rs - 1, "--", color="#d62728", lw=1.4, label=r"$r-1$")
    ax1.set_title(r"Lemma: $\lfloor rb/s\rfloor+\lfloor ra/s\rfloor = r-1$")
    ax1.set_xlabel("r"); ax1.set_ylabel("value"); ax1.legend(); ax1.grid(alpha=0.25)

    ax2.plot(rs, frac_sum, "o-", color="#9467bd")
    ax2.axhline(1.0, color="#d62728", ls="--", lw=1.4)
    ax2.set_ylim(0, 1.3)
    ax2.set_title(r"$\{rb/s\}+\{ra/s\}=1$  (since $\gcd(s,a)=\gcd(s,b)=1$)")
    ax2.set_xlabel("r"); ax2.set_ylabel("fractional-part sum"); ax2.grid(alpha=0.25)
    fig.suptitle(f"Why the closed form is exact  (a={a}, b={b}, s=a+b={s})",
                 fontsize=12)
    fig.tight_layout()
    fig.savefig(os.path.join(FIG, "fig4_invariant.png"), dpi=130)
    plt.close(fig)


# ---------------------------------------------------------------------------
def fig_benchmark():
    """Fig 5: measured scaling - formula O(1) vs binary search O(log n)."""
    a, b = 99991, 99989  # note: not coprime? ensure coprime
    from math import gcd
    if gcd(a, b) != 1:
        b = 99989
    ns = np.unique(np.logspace(1, 7, 30).astype(int))
    reps = 2000
    t_formula, t_binary = [], []
    for n in ns:
        n = int(n)
        t0 = time.perf_counter()
        for _ in range(reps):
            formula(a, b, n)
        t_formula.append((time.perf_counter() - t0) / reps * 1e6)  # us/call
        t0 = time.perf_counter()
        for _ in range(reps):
            binary_search(a, b, n)
        t_binary.append((time.perf_counter() - t0) / reps * 1e6)
    fig, ax = plt.subplots(figsize=(9, 5.5))
    ax.plot(ns, t_binary, "o-", color="#1f77b4", label="binary search  O(log n)")
    ax.plot(ns, t_formula, "s-", color="#2ca02c", label="formula  O(1)")
    ax.set_xscale("log")
    ax.set_xlabel("n (index)")
    ax.set_ylabel("time per call (microseconds)")
    ax.set_title("Measured scaling (Python): formula is flat, binary grows with log n")
    ax.legend(); ax.grid(alpha=0.25, which="both")
    fig.tight_layout()
    fig.savefig(os.path.join(FIG, "fig5_benchmark.png"), dpi=130)
    plt.close(fig)
    return ns, t_binary, t_formula


if __name__ == "__main__":
    fig_number_line()
    print("fig1_number_line.png")
    fig_period()
    print("fig2_period.png")
    fig_staircase()
    print("fig3_staircase.png")
    fig_invariant()
    print("fig4_invariant.png")
    ns, tb, tf = fig_benchmark()
    print("fig5_benchmark.png")
    print(f"  binary: {tb[0]:.2f}->{tb[-1]:.2f} us/call ; "
          f"formula: {min(tf):.2f}-{max(tf):.2f} us/call (flat)")
    print("All figures written to docs/figures/")
