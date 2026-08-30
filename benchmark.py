"""Benchmark: binary search vs. formula, with correctness cross-check.

Reads whitespace-separated (a b n) triples from a file (default test_cases.txt,
or pass a path as argv[1]).  Enforces a=min, b=max per case.  Times each method
over all cases, verifies the two agree, and reports totals.

Usage:
    python -m termboost.testgen --count 200000 --out test_cases.txt
    python benchmark.py test_cases.txt
"""
import os
import sys
import time

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))
from termboost.algorithms import binary_search, formula  # noqa: E402


def load(path):
    with open(path) as f:
        toks = f.read().split()
    it = iter(toks)
    cases = []
    for a in it:
        b = next(it)
        n = next(it)
        a, b, n = int(a), int(b), int(n)
        cases.append((min(a, b), max(a, b), n))
    return cases


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else "test_cases.txt"
    if not os.path.exists(path):
        sys.exit(f"no test file '{path}' - generate with "
                 f"`python -m termboost.testgen --out {path}`")
    cases = load(path)

    t0 = time.perf_counter()
    bin_ans = [binary_search(a, b, n) for a, b, n in cases]
    t_binary = (time.perf_counter() - t0) * 1000

    t0 = time.perf_counter()
    for_ans = [formula(a, b, n) for a, b, n in cases]
    t_formula = (time.perf_counter() - t0) * 1000

    mismatches = 0
    for (a, b, n), x1, x2 in zip(cases, bin_ans, for_ans):
        if x1 != x2:
            mismatches += 1
            if mismatches <= 10:
                print(f"MISMATCH (a={a}, b={b}, n={n}): binary={x1} formula={x2}")

    print(f"Total test cases: {len(cases)}")
    print(f"Binary Search time:  {t_binary:10.2f} ms")
    print(f"Formula-Based time:  {t_formula:10.2f} ms")
    if t_formula > 0:
        print(f"Speedup (binary/formula): {t_binary / t_formula:.1f}x")
    print(f"Mismatches: {mismatches}")


if __name__ == "__main__":
    main()
