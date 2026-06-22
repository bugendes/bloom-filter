#!/usr/bin/env python3
"""Bloom Filter — probabilistic set membership."""
import hashlib, math

class BloomFilter:
    def __init__(self, expected=100000, fp_rate=0.01):
        self.size = int(-expected * math.log(fp_rate) / (math.log(2)**2))
        self.k = max(1, int(self.size / expected * math.log(2)))
        self.bits = bytearray(self.size // 8 + 1)
        self.count = 0

    def _hashes(self, item):
        h1 = int(hashlib.md5(str(item).encode()).hexdigest(), 16)
        h2 = int(hashlib.sha256(str(item).encode()).hexdigest(), 16)
        return [(h1 + i * h2) % self.size for i in range(self.k)]

    def add(self, item):
        for idx in self._hashes(item):
            self.bits[idx // 8] |= (1 << (idx % 8))
        self.count += 1

    def __contains__(self, item):
        return all(self.bits[idx // 8] & (1 << (idx % 8)) for idx in self._hashes(item))

if __name__ == "__main__":
    N = 100000
    bf = BloomFilter(N, 0.01)
    for i in range(N): bf.add(f"item_{i}")
    fps = sum(1 for i in range(N, N*2) if f"item_{i}" in bf)
    print(f"Bloom Filter: {N:,} items, FP rate: {fps/N*100:.2f}% (expected 1%)")\n