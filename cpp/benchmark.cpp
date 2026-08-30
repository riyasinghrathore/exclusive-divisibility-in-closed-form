// benchmark.cpp
//
// TermBoost: find the n-th positive integer divisible by exactly one of
// (a, b) -- i.e. divisible by a XOR divisible by b -- where a < b,
// gcd(a, b) == 1, a, b > 1, n > 0. All arithmetic uses long long (int64).
//
// Provides three implementations:
//   1. bruteForce   - reference oracle, O(answer), used only for self-test.
//   2. binarySearch - O(log(n*a)) using an inclusion-exclusion counting
//                      function inside a binary search.
//   3. formula      - the novel O(1) closed-form solution.
//
// Build:
//   g++ -O2 -std=c++17 -o benchmark benchmark.cpp
// Run:
//   ./benchmark [path/to/test_cases.txt]   (defaults to "test_cases.txt")

#include <algorithm>
#include <chrono>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <string>
#include <vector>

using namespace std;

// ---------------------------------------------------------------------------
// 1. Brute force reference oracle (slow). Iterates num = 1, 2, 3, ...
//    counting numbers where exactly one of (num % a == 0), (num % b == 0)
//    holds (XOR). Returns the num at which the count reaches n.
// ---------------------------------------------------------------------------
long long bruteForce(long long a, long long b, long long n) {
    long long count = 0;
    long long num = 0;
    while (count < n) {
        ++num;
        bool divA = (num % a == 0);
        bool divB = (num % b == 0);
        if (divA != divB) { // XOR: exactly one of the two
            ++count;
        }
    }
    return num;
}

// ---------------------------------------------------------------------------
// 2. Binary search. Counts how many valid numbers (divisible by exactly one
//    of a, b) are <= x using inclusion-exclusion:
//       count(x) = x/a + x/b - 2*(x/(a*b))
//    then binary searches for the smallest x with count(x) >= n.
// ---------------------------------------------------------------------------
static inline long long countUpTo(long long x, long long a, long long b, long long ab) {
    return x / a + x / b - 2 * (x / ab);
}

long long binarySearch(long long a, long long b, long long n) {
    long long ab = a * b;
    long long lo = 0, hi = n * a;
    while (lo < hi) {
        long long mid = lo + (hi - lo) / 2; // avoid overflow-prone (lo+hi)/2 issues
        if (countUpTo(mid, a, b, ab) < n) {
            lo = mid + 1;
        } else {
            hi = mid;
        }
    }
    return lo;
}

// ---------------------------------------------------------------------------
// 3. Closed-form O(1) formula (the novel method).
//
//    Within each period of length a*b there are exactly p = a + b - 2 valid
//    numbers (numbers divisible by exactly one of a, b). We find which full
//    period the n-th valid number falls in (q), and its rank r within that
//    period (1-indexed, r in [1, p]). Then we locate the r-th valid value
//    within the period directly via a closed-form index computation.
// ---------------------------------------------------------------------------
long long formula(long long a, long long b, long long n) {
    long long s = a + b;
    long long p = a + b - 2; // valid numbers per period of length a*b
    long long q = (n - 1) / p;
    long long r = n - q * p; // r is in [1, p]
    long long i = (r * b) / s;
    long long j = (r * a) / s;
    long long Vr = min(a * (i + 1), b * (j + 1));
    return q * (a * b) + Vr;
}

// ---------------------------------------------------------------------------
// Self-test: small brute-force comparison at startup.
// ---------------------------------------------------------------------------
static bool selfTest() {
    for (long long a = 2; a <= 30; ++a) {
        for (long long b = a + 1; b <= 30; ++b) {
            // enforce gcd(a, b) == 1
            long long x = a, y = b;
            while (y) { long long t = x % y; x = y; y = t; }
            if (x != 1) continue; // not coprime, skip

            for (long long n = 1; n <= 100; ++n) {
                long long bf = bruteForce(a, b, n);
                long long bs = binarySearch(a, b, n);
                long long fm = formula(a, b, n);
                if (bf != bs || bf != fm) {
                    cout << "self-test MISMATCH at a=" << a << " b=" << b
                         << " n=" << n << " : bruteForce=" << bf
                         << " binarySearch=" << bs << " formula=" << fm
                         << endl;
                    return false;
                }
            }
        }
    }
    cout << "self-test passed" << endl;
    return true;
}

// ---------------------------------------------------------------------------
// main: load test cases, run self-test, verify, and benchmark.
// ---------------------------------------------------------------------------
int main(int argc, char** argv) {
    // 1. Small self-test comparing all three implementations.
    selfTest();

    // 2. Load test cases from file.
    string path = (argc > 1) ? argv[1] : "test_cases.txt";
    ifstream in(path);
    if (!in) {
        cerr << "Could not open test case file: " << path << endl;
        return 1;
    }

    struct Case { long long a, b, n; };
    vector<Case> cases;
    long long a, b, n;
    while (in >> a >> b >> n) {
        if (a > b) swap(a, b); // enforce a = min, b = max
        cases.push_back({a, b, n});
    }

    if (cases.empty()) {
        cerr << "No test cases loaded from " << path << endl;
        return 1;
    }

    // 3. Verify binarySearch == formula for every case.
    bool allMatch = true;
    for (auto& c : cases) {
        long long bs = binarySearch(c.a, c.b, c.n);
        long long fm = formula(c.a, c.b, c.n);
        if (bs != fm) {
            allMatch = false;
            cout << "MISMATCH case a=" << c.a << " b=" << c.b << " n=" << c.n
                 << " : binarySearch=" << bs << " formula=" << fm << endl;
        }
    }
    if (allMatch) {
        cout << "verification passed: binarySearch == formula for all "
             << cases.size() << " cases" << endl;
    }

    // 4. Benchmark: total wall time for binarySearch and formula over all cases.
    volatile long long sinkBS = 0;
    volatile long long sinkFM = 0;

    auto t0 = chrono::steady_clock::now();
    for (auto& c : cases) {
        sinkBS += binarySearch(c.a, c.b, c.n);
    }
    auto t1 = chrono::steady_clock::now();
    for (auto& c : cases) {
        sinkFM += formula(c.a, c.b, c.n);
    }
    auto t2 = chrono::steady_clock::now();

    double bsMs = chrono::duration<double, milli>(t1 - t0).count();
    double fmMs = chrono::duration<double, milli>(t2 - t1).count();
    double speedup = (fmMs > 0.0) ? (bsMs / fmMs) : 0.0;

    cout << "total cases: " << cases.size() << endl;
    cout << "binarySearch total time: " << bsMs << " ms" << endl;
    cout << "formula total time: " << fmMs << " ms" << endl;
    cout << "speedup factor (binarySearch / formula): " << speedup << endl;

    // Prevent the sinks from being flagged unused (they are volatile, so the
    // compiler already can't drop the accumulation, but silence -Wunused).
    (void)sinkBS;
    (void)sinkFM;

    return allMatch ? 0 : 2;
}
