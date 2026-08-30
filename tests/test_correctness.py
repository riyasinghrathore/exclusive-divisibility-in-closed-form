"""Correctness tests: formula == binary_search == brute_force.

Run with:  pytest -q      (from the repo root, with src on the path)
or standalone:  python tests/test_correctness.py
"""
import os
import random
import sys
from math import gcd

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from termboost.algorithms import brute_force, binary_search, formula  # noqa: E402


def coprime_pairs(limit):
    for a in range(2, limit):
        for b in range(a + 1, limit):
            if gcd(a, b) == 1:
                yield a, b


def test_exhaustive_small_grid():
    """Every coprime pair up to 50, every n up to 2.5 periods, vs brute force."""
    for a, b in coprime_pairs(50):
        upper = 2 * (a + b - 2) + 5  # cover >2 full periods incl. boundaries
        for n in range(1, upper + 1):
            bf = brute_force(a, b, n)
            assert formula(a, b, n) == bf, (a, b, n, "formula", formula(a, b, n), bf)
            assert binary_search(a, b, n) == bf, (a, b, n, "binary", bf)


def test_period_boundaries():
    """n exactly at / around multiples of the period p = a+b-2."""
    for a, b in coprime_pairs(60):
        p = a + b - 2
        for k in range(0, 4):
            for delta in (-1, 0, 1):
                n = k * p + delta
                if n < 1:
                    continue
                bf = brute_force(a, b, n)
                assert formula(a, b, n) == bf, (a, b, n)


def test_large_n_formula_vs_binary():
    """Large random cases: formula vs binary search (both fast, no brute)."""
    rng = random.Random(20260831)
    checked = 0
    for _ in range(50000):
        a = rng.randint(2, 100000)
        b = rng.randint(2, 100000)
        if a == b or gcd(a, b) != 1:
            continue
        if a > b:
            a, b = b, a
        n = rng.randint(1, 10_000_000)
        assert formula(a, b, n) == binary_search(a, b, n), (a, b, n)
        checked += 1
    assert checked > 1000


def test_answer_is_valid_and_nth():
    """Sanity: the returned value is itself valid and has the right rank."""
    from termboost.algorithms import count_up_to
    rng = random.Random(7)
    for _ in range(2000):
        a = rng.randint(2, 500)
        b = rng.randint(2, 500)
        if a == b or gcd(a, b) != 1:
            continue
        if a > b:
            a, b = b, a
        n = rng.randint(1, 5000)
        x = formula(a, b, n)
        assert (x % a == 0) ^ (x % b == 0)          # x is valid
        assert count_up_to(a, b, x) == n            # x is the n-th
        assert count_up_to(a, b, x - 1) == n - 1    # nothing valid in (x-1, x)


if __name__ == "__main__":
    test_exhaustive_small_grid()
    print("exhaustive small grid: OK")
    test_period_boundaries()
    print("period boundaries: OK")
    test_answer_is_valid_and_nth()
    print("validity/rank: OK")
    test_large_n_formula_vs_binary()
    print("large random formula-vs-binary: OK")
    print("ALL PASSED")
