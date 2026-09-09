"""Generate benchmark test cases: coprime (a, b) with a mix of small/medium/large n.

Mirrors the constraints in the paper:
    2 <= a, b <= 100000,  gcd(a, b) = 1,  1 <= n <= 10_000_000

Usage:
    python -m termboost.testgen --count 1000000 --out test_cases.txt --seed 42
"""
import argparse
import random
from math import gcd


def gen_case(rng):
    while True:
        a = rng.randint(2, 100_000)
        b = rng.randint(2, 100_000)
        if a == b or gcd(a, b) != 1:
            continue
        if a > b:
            a, b = b, a
        bucket = rng.random()
        if bucket < 0.34:          # small
            n = rng.randint(1, 1_000)
        elif bucket < 0.67:        # medium
            n = rng.randint(1_000, 1_000_000)
        else:                      # large
            n = rng.randint(1_000_000, 10_000_000)
        return a, b, n


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--count", type=int, default=1_000_000)
    ap.add_argument("--out", default="test_cases.txt")
    ap.add_argument("--seed", type=int, default=42)
    args = ap.parse_args()

    rng = random.Random(args.seed)
    with open(args.out, "w") as f:
        for _ in range(args.count):
            a, b, n = gen_case(rng)
            f.write(f"{a} {b} {n}\n")
    print(f"wrote {args.count} cases to {args.out}")


if __name__ == "__main__":
    main()
