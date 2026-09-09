"""TermBoost algorithms.

Problem
-------
Given co-prime integers ``a`` and ``b`` (``1 < a < b``, ``gcd(a, b) = 1``) and an
index ``n > 0``, return the ``n``-th smallest positive integer that is divisible
by ``a`` or ``b`` but *not* both.

This module provides three implementations:

* :func:`brute_force`   -- the O(answer) reference oracle.
* :func:`binary_search` -- the existing O(log N) baseline.
* :func:`formula`       -- the novel O(1) closed form (see ``PROOF.md``).

The driver code enforces ``a < b``; every function assumes that ordering.
"""

from math import gcd as _gcd

__all__ = ["gcd", "lcm", "count_up_to", "brute_force", "binary_search", "formula"]


def gcd(a: int, b: int) -> int:
    """Greatest common divisor."""
    return _gcd(a, b)


def lcm(a: int, b: int) -> int:
    """Least common multiple. For coprime ``a, b`` this is simply ``a * b``."""
    return a // _gcd(a, b) * b


def count_up_to(a: int, b: int, x: int) -> int:
    """Number of valid integers in ``[1, x]``.

    A "valid" integer is divisible by ``a`` or ``b`` but not both.  Because
    ``a`` and ``b`` are coprime, "divisible by both" is exactly "divisible by
    ``a*b``".  Inclusion-exclusion, subtracting the shared multiples *twice*
    (once from each list) so they are excluded rather than merely deduplicated::

        C(x) = floor(x/a) + floor(x/b) - 2 * floor(x / (a*b))
    """
    return x // a + x // b - 2 * (x // (a * b))


def brute_force(a: int, b: int, n: int) -> int:
    """Reference oracle: scan the integers counting valid ones (1-indexed)."""
    count = 0
    num = 0
    while True:
        num += 1
        if (num % a == 0) ^ (num % b == 0):
            count += 1
            if count == n:
                return num


def binary_search(a: int, b: int, n: int) -> int:
    """Existing baseline: binary search for the smallest ``x`` with ``C(x) = n``.

    ``C`` is non-decreasing, so we find the least ``x`` with ``C(x) >= n``.  That
    ``x`` is necessarily a valid number (``C`` only increases when it lands on
    one), hence it is the answer.  Complexity ``O(log(n*a))``.
    """
    lo, hi = 0, n * a
    while lo < hi:
        mid = (lo + hi) // 2
        if count_up_to(a, b, mid) < n:
            lo = mid + 1
        else:
            hi = mid
    return lo


def formula(a: int, b: int, n: int) -> int:
    """Novel O(1) closed form.  Proof of correctness in ``PROOF.md``.

    Structure of the proof:

    * The valid set is periodic with period ``a*b`` and contains exactly
      ``p = a + b - 2`` valid numbers per period.
    * Strip whole periods:  ``q = (n-1)//p`` full periods contribute
      ``q * a*b``; let ``r = n - q*p`` be the 1-based index within the period,
      ``r in [1, p]``.
    * Within a period the ``r``-th valid number is
      ``min(a*(i+1), b*(j+1))`` where ``i = floor(r*b/s)``,
      ``j = floor(r*a/s)`` and ``s = a + b``.  The key lemma is
      ``i + j = r - 1`` (uses ``gcd(a+b, a) = gcd(a+b, b) = 1``).
    """
    s = a + b
    p = a + b - 2  # valid numbers per period of length a*b
    q, r = divmod(n - 1, p)
    r += 1  # r in [1, p]
    i = (r * b) // s
    j = (r * a) // s
    vr = min(a * (i + 1), b * (j + 1))
    return q * (a * b) + vr
