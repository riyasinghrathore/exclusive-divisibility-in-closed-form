# Proof: the O(1) formula for the n-th coprime-exclusive multiple

## What this repo is

`termboost` benchmarks two ways of answering the same question — a
binary-search baseline (`Main.binaryApproach`) and a closed-form, O(1)
formula I derived (`Main.trUE_n_Smallest_AB`) — and this document plus
[`proof/proof.py`](proof/proof.py) is the proof that the formula is
actually correct, not just fast.

The full written derivation, with an interactive slider-driven visual proof,
lives on my site:
**[TermBoost: The n-th Coprime-Exclusive Multiple in O(1)](https://TODO-replace-with-your-live-site-domain/articles/termboost-nth-coprime-multiple.html)**
<!-- TODO: swap in the live URL once the site is deployed; the article
     source is research-site/articles/termboost-nth-coprime-multiple.html. -->
That page derives the formula step by step in prose. This document instead
proves it computationally: symbolically, numerically, and graphically, in
Python, independent of the Java implementation.

## Problem statement

Fix two coprime integers `a, b > 1` with `a < b`, and a positive integer `n`.
Find the `n`-th smallest positive integer divisible by `a` or by `b`, but
not both.

For `a=2, b=3`: `2, 3, 4, 8, 9, 10, 14, 15, 16, ...` — `6` and `12` are
skipped (multiples of both).

Everything below rests on one function, the count of qualifying integers
in `[1, x]`:

```
count(x) = floor(x/a) + floor(x/b) - 2 * floor(x/(ab))
```

(subtracting the "both" term *twice* — once to undo ordinary
inclusion–exclusion's single subtraction, once more to remove it from the
tally entirely, since we want "exactly one" divisor, not "at least one").

## Step 1 — count(x) is flat except at qualifying integers

**Claim:** `count(x) - count(x-1)` is `1` if `x` is divisible by exactly one
of `a, b`, and `0` otherwise.

This is what makes "smallest `x` with `count(x) >= n`" the *same* problem as
"the `n`-th qualifying integer," with no off-by-one patching needed — a
single floor-value increase always lands exactly on a hit.

`proof/proof.py::symbolic_flatness_argument` checks this directly: for a
handful of coprime `(a, b)` pairs, it walks `x` across three full periods
and confirms `count(x) - count(x-1)` matches the exactly-one-divisor
indicator at every single integer, not just on average.

```
$ python3 proof/proof.py
=== 1. Symbolic flatness argument ===
  a=2, b=3: step matches indicator over 3*ab range -> OK
  a=3, b=5: step matches indicator over 3*ab range -> OK
  a=4, b=7: step matches indicator over 3*ab range -> OK
  a=5, b=8: step matches indicator over 3*ab range -> OK
```

![count(x) staircase](proof/figures/count_staircase.png)

*`count(x)` for `a=2, b=3, n=12`: every step is height exactly 1, and the
step lands exactly where the dashed target line (`n`) meets the answer
(`x = 22`).*

## Step 2 — the sequence is periodic with period ab

If `x` qualifies (divisible by exactly one of `a, b`), so does `x + ab`:
adding a multiple of `ab` changes divisibility by neither `a` nor `b`. So
the whole problem reduces to solving it once inside a window `(0, ab]`,
then translating by however many full windows are skipped.

Inside `(0, ab)` there are `b-1` multiples of `a` and `a-1` multiples of
`b`, and — because `gcd(a,b)=1` — none of them coincide except at the
boundary `ab` itself. So **every one** of these `a+b-2` multiples
qualifies; that constant is exactly the number of qualifying terms per
period.

![periodic block structure](proof/figures/periodic_blocks.png)

*`a=3, b=5`: multiples of `a` (blue, above the line) and multiples of `b`
(orange, below), repeating identically every `ab = 15` — always
`a+b-2 = 6` qualifying points per window, never touching at the shared
multiple of `ab`.*

Peeling off `k = floor(n / (a+b-2))` whole windows contributes `k*ab` to
the answer (the `filler` term in the code) and leaves a residual index
`r = n mod (a+b-2)` to be found inside the *next* window.

## Step 3 — solving inside one window without a search

What's left: find the `r`-th smallest element of the merged, sorted set
`{a, 2a, ...} ∪ {b, 2b, ...}`. The exact integer answer `v` satisfies
`floor(v/a) + floor(v/b) = r`. Dropping the floors and solving the
*continuous* relaxation `v/a + v/b = r` gives a closed form:

```
$ python3 proof/proof.py
=== 2. Continuous relaxation ===
  Solving v/a + v/b = r for v gives v0 = a*b*r/(a + b)
  => v0/a = b*r/(a + b),  v0/b = a*r/(a + b)
  These match rat_a = (n*b)/(a+b) and rat_b = (n*a)/(a+b) in trUE_n_Smallest_AB.
```

`proof.py::symbolic_continuous_relaxation` derives `v0 = r·ab/(a+b)`
symbolically with sympy rather than by hand, then confirms
`v0/a` and `v0/b` are literally the `rat_a`/`rat_b` expressions used in the
Java (and Python port) code.

Truncating `v0/a` and `v0/b` estimates how many multiples of `a` and of `b`
have been consumed by position `r`. Because `v0` solves the relaxed
equation *exactly*, the floor-truncation error stays bounded — small enough
that the true answer is always one of exactly two candidates: the next
unconsumed multiple of `a`, or the next unconsumed multiple of `b`. A single
comparison (`a*rat_a` vs `b*rat_b`) picks the right one.

![relaxation margin](proof/figures/relaxation_margin.png)

*`a=7, b=11`: left, the continuous relaxation `v0` (line) tracks the true
integer answer (dots) closely across a full window; right, the gap between
them stays well under the `max(a, b)` bound `proof.py::plot_relaxation_margin`
checks numerically — which is exactly why only two candidates ever need
comparing.*

## Step 4 — exhaustive numeric verification

Steps 1–3 explain *why* the formula works. As a final, independent check
(deliberately re-implemented in Python rather than shared with the Java, so
the two can't hide a common bug), `proof.py::numeric_cross_check`
brute-force-verifies `true_n_smallest_ab` against a direct enumeration
across hundreds of random coprime pairs and a spread of `n`:

```
$ python3 proof/proof.py
=== 3. Numeric cross-check (independent Python re-implementation) ===
  Checked 4500 (a, b, n) triples across 300 coprime pairs.
  All matched. No counterexample found.
```

The Java side runs the same kind of check at much larger scale — see the
[benchmark section of the README](README.md#benchmark): 1,000,000 randomly
generated coprime pairs, zero mismatches between `binaryApproach` and
`trUE_n_Smallest_AB`.

## Reproducing this document

```sh
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python3 proof/proof.py
```

This regenerates all three figures in `proof/figures/` and reprints every
transcript block quoted above.
