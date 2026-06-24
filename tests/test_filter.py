"""Tests for BloomFilter."""

import pytest
from bloom_filter import BloomFilter


class TestBloomFilter:
    def test_no_false_negatives(self):
        bf = BloomFilter(1000, 0.01)
        for i in range(100):
            bf.add(f"item_{i}")
        for i in range(100):
            assert f"item_{i}" in bf

    def test_false_positive_rate(self):
        bf = BloomFilter(10000, 0.01)
        for i in range(10000):
            bf.add(i)
        false_positives = sum(1 for i in range(10000, 20000) if i in bf)
        rate = false_positives / 10000
        assert rate < 0.05  # should be around 0.01

    def test_contains_operator(self):
        bf = BloomFilter(100)
        bf.add("hello")
        assert "hello" in bf
        assert "world" not in bf  # high probability

    def test_size(self):
        bf = BloomFilter(100)
        assert len(bf) == 0
        bf.add("x")
        assert len(bf) == 1

    def test_clear(self):
        bf = BloomFilter(100)
        bf.add("x")
        bf.clear()
        assert len(bf) == 0

    def test_optimal_params(self):
        bf = BloomFilter(1000, 0.01)
        assert bf.num_hashes >= 1
        assert bf.bit_array_size > 0
