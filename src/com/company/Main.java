package com.company;

import java.io.*;
import java.util.*;


public class Main {

    // Function to compute GCD (Greatest Common Divisor)
    private static long gcd(long a, long b) {
        if (b == 0) return a;
        return gcd(b, a % b);
    }

    // Function to compute LCM (Least Common Multiple)
    private static long lcm(long a, long b) {
        return (a / gcd(a, b)) * b;
    }

    // Function to get the nth number divisible by a or b (but not both)
    public static long findNthTerm(long a, long b, long n) {
        long count = 0, num = 1;
        long lcm = lcm(a, b);

        while (count < n) {
            if ((num % a == 0 || num % b == 0) && num % lcm != 0) {
                count++;
            }
            if (count == n) return num; // Return nth valid term
            num++;
        }
        return -1; // Should never reach here
    }

    // Function to validate if a given result is correct
    public static boolean isValidResult(long a, long b, long n, long candidate) {
        long expectedNthTerm = findNthTerm(a, b, n);
        return expectedNthTerm == candidate;
    }
    public static long binaryApproach(long a, long b, long n, long low, long high) {
        while (low < high) {
            long mid = (low + high) / 2;
            long count = (mid / a) + (mid / b) - 2 * (mid / (a * b));  // Use a * b directly

            if (count < n) {
                low = mid + 1;
            } else {
                high = mid;
            }
        }

        // Adjust 'low' to the nearest valid number divisible by 'a' or 'b'
        if (low % a == 0 || low % b == 0) return low;
        return Math.min(a * (low / a + 1), b * (low / b + 1));
    }

    public static long binaryApproach_old(long a, long b, long n, long low,
                                      long high){

        long mid = (low + high)/2;
        if (mid/a + mid/b - 2*(mid/(a*b)) == n){
            if (mid % a == 0 || mid % b == 0){
                return mid;}
            else {
                return Math.max(a*(mid/a), b*(mid/b));
            }
        }

        else if (mid/a + mid/b - 2*(mid/(a*b)) > n){
            return binaryApproach(a, b, n, low, mid);
        }
        else {
            return binaryApproach(a, b, n, mid + 1, high);
        }
    }

    public static long trUE_n_Smallest_AB(long a, long b, long n){
        if (n*a < b){return n*a;}
        if (n*a == b){return a*(n+1);}

        long filler = 0;
        long sum = 0;
        if (n > a+b-2) {
            sum = a + b -2; filler = (n/sum)*a*b; n %= sum;}
        if (n == 0){
            return filler - a;
        }
        long rat_a = (n*b)/(a+b);
        long rat_b = (n*a)/(a+b);
        if(a*rat_a > b*rat_b){
            return (Math.min(a*rat_a+a ,b*rat_b + b) + filler);
        } else {
            return (a*rat_a + a + filler);
        }
    }

    // Benchmark test cases
    public static void benchmark(String filename) throws IOException {
        File file = new File(filename);
        Scanner sc = new Scanner(file);
        List<long[]> testCases = new ArrayList<>();

        while (sc.hasNextLong()) {
            long a = sc.nextLong();
            long b = sc.nextLong();
            long n = sc.nextLong();
            testCases.add(new long[]{a, b, n});
        }
        sc.close();

        long totalBinaryTime = 0, totalFormulaTime = 0;
        int testCount = testCases.size();

        for (long[] testCase : testCases) {
            long a = Math.min(testCase[0], testCase[1]);
            long b = Math.max(testCase[0], testCase[1]);
            long n = testCase[2];

            // Binary Search Benchmark
            long startTime1 = System.nanoTime();
            long answer1 = binaryApproach(a, b, n, 0, n * a);
            long endTime1 = System.nanoTime();
            totalBinaryTime += (endTime1 - startTime1);

            // Formula-Based Benchmark
            long startTime2 = System.nanoTime();
            long answer2 = trUE_n_Smallest_AB(a, b, n);
            long endTime2 = System.nanoTime();
            totalFormulaTime += (endTime2 - startTime2);

            // Validate outputs
            if (answer1 != answer2) {
                boolean a1_correct = isValidResult(a, b, n, answer1);
                boolean a2_correct = isValidResult(a, b, n, answer2);
                if (a1_correct){
                    System.out.println("Binary wins");
                } else if (a2_correct) {
                    System.out.println("Formula wins");
                } else {
                    System.out.println("No one wins");
                }
                System.out.println("Mismatch for (" + a + ", " + b + ", " + n + ")");
                System.out.println("Binary: " + answer1 + ", Formula: " + answer2);
            }
        }

        System.out.println("Total test cases: " + testCount);
        System.out.println("Binary Approach Time: " + totalBinaryTime / 1_000_000.0 + " ms");
        System.out.println("Formula-Based Approach Time: " + totalFormulaTime / 1_000_000.0 + " ms");
    }

    public static void main(String[] args) {
        String filename = "src/com/company/test_cases.txt";

        try {
            benchmark(filename); // Run benchmarks
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
