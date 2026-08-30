package com.company;

import java.io.FileWriter;
import java.io.IOException;
import java.util.Random;

/**
 * Generates random (a, b, n) benchmark cases for Main.benchmark(...).
 *
 * Constraints match the ones described in the README:
 *   - 2 <= a, b <= 100_000
 *   - gcd(a, b) == 1  (coprime)
 *   - 1 <= n <= 10_000_000, drawn across small/medium/large bands so the
 *     benchmark isn't dominated by one regime.
 *
 * Output: whitespace-separated "a b n" triples, one per line, written to
 * src/com/company/test_cases.txt (the path Main.benchmark(...) reads by
 * default).
 */
public class TestCaseGenerator {

    private static final int MIN_AB = 2;
    private static final int MAX_AB = 100_000;

    private static long gcd(long a, long b) {
        while (b != 0) {
            long t = b;
            b = a % b;
            a = t;
        }
        return a;
    }

    private static int randomN(Random rnd) {
        // Mix of small / medium / large n so the benchmark exercises all
        // three bands called out in the README.
        double band = rnd.nextDouble();
        if (band < 0.34) {
            return 1 + rnd.nextInt(1_000);                     // small: [1, 1_000]
        } else if (band < 0.67) {
            return 1_000 + rnd.nextInt(1_000_000 - 1_000);      // medium: [1_000, 1_000_000)
        } else {
            return 1_000_000 + rnd.nextInt(10_000_000 - 1_000_000 + 1); // large: [1_000_000, 10_000_000]
        }
    }

    public static void main(String[] args) throws IOException {
        int count = args.length > 0 ? Integer.parseInt(args[0]) : 1_000_000;
        String outPath = args.length > 1 ? args[1] : "src/com/company/test_cases.txt";

        Random rnd = new Random(42); // fixed seed -> reproducible benchmark runs
        try (FileWriter out = new FileWriter(outPath)) {
            for (int i = 0; i < count; i++) {
                long a, b;
                do {
                    a = MIN_AB + rnd.nextInt(MAX_AB - MIN_AB + 1);
                    b = MIN_AB + rnd.nextInt(MAX_AB - MIN_AB + 1);
                } while (a == b || gcd(a, b) != 1);

                int n = randomN(rnd);
                out.write(a + " " + b + " " + n + "\n");
            }
        }

        System.out.println("Wrote " + count + " test cases to " + outPath);
    }
}
