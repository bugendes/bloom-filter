#!/usr/bin/env python3
"""Bloom Filter demo."""

from bloom_filter import BloomFilter


def main():
    print("=== Bloom Filter Demo ===
")

    bf = BloomFilter(expected_elements=10000, false_positive_rate=0.01)
    print(f"Bit array size: {bf.bit_array_size}")
    print(f"Hash functions: {bf.num_hashes}")

    words = ["apple", "banana", "cherry", "date", "elderberry"]
    for w in words:
        bf.add(w)

    test = ["apple", "banana", "fig", "grape", "cherry"]
    for w in test:
        result = "probably yes" if w in bf else "definitely no"
        print(f"  contains('{w}'): {result}")

    print(f"
Estimated FP rate: {bf.estimated_fp_rate:.6f}")


if __name__ == "__main__":
    main()
