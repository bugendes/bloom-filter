"""Bloom Filter implementation.

A space-efficient probabilistic data structure that tests set membership.
False positives are possible; false negatives are not.

Uses k independent hash functions mapped onto a bit array of size m.
The optimal number of hash functions: k = (m/n) * ln(2), where n is the
expected number of elements.

False positive probability: p ≈ (1 - e^(-kn/m))^k

Time complexity:
  - add: O(k) — k hash computations
  - contains: O(k)
  - no delete (use Counting Bloom Filter for that)

Space: O(m) bits, where m is the bit array size.

Used in: databases, networks, spell checkers, URL crawlers, bioinformatics.
"""

from __future__ import annotations

import hashlib
import math
from typing import Hashable


class BloomFilter:
    """Space-efficient probabilistic set membership.

    Args:
        expected_elements: Estimated number of insertions (n).
        false_positive_rate: Desired false positive probability (p).
    """

    def __init__(self, expected_elements: int, false_positive_rate: float = 0.01) -> None:
        if expected_elements <= 0:
            raise ValueError("expected_elements must be positive")
        if not (0 < false_positive_rate < 1):
            raise ValueError("false_positive_rate must be in (0, 1)")

        self._n = expected_elements
        self._p = false_positive_rate

        # Optimal bit array size: m = -n*ln(p) / (ln2)^2
        self._m = max(1, int(-expected_elements * math.log(false_positive_rate) / (math.log(2) ** 2)))

        # Optimal number of hash functions: k = (m/n) * ln2
        self._k = max(1, int((self._m / expected_elements) * math.log(2)))

        self._bits = bytearray((self._m + 7) // 8)
        self._count = 0

    @property
    def size(self) -> int:
        """Number of elements added."""
        return self._count

    @property
    def bit_array_size(self) -> int:
        """Size of the underlying bit array (m)."""
        return self._m

    @property
    def num_hashes(self) -> int:
        """Number of hash functions (k)."""
        return self._k

    @property
    def estimated_fp_rate(self) -> float:
        """Current estimated false positive rate."""
        if self._count == 0:
            return 0.0
        return (1 - math.exp(-self._k * self._count / self._m)) ** self._k

    def _hash_indices(self, item: Hashable) -> list[int]:
        """Generate k hash positions using double hashing (Kirsch-Mitzenmacker)."""
        data = str(item).encode("utf-8")
        h1 = int(hashlib.md5(data).hexdigest(), 16)
        h2 = int(hashlib.sha256(data).hexdigest(), 16)
        return [(h1 + i * h2) % self._m for i in range(self._k)]

    def _set_bit(self, idx: int) -> None:
        byte_idx = idx >> 3
        bit_idx = idx & 7
        self._bits[byte_idx] |= (1 << bit_idx)

    def _get_bit(self, idx: int) -> bool:
        byte_idx = idx >> 3
        bit_idx = idx & 7
        return bool(self._bits[byte_idx] & (1 << bit_idx))

    def add(self, item: Hashable) -> None:
        """Add an element to the filter."""
        for idx in self._hash_indices(item):
            self._set_bit(idx)
        self._count += 1

    def contains(self, item: Hashable) -> bool:
        """Test membership. Returns True if probably present, False if definitely absent."""
        return all(self._get_bit(idx) for idx in self._hash_indices(item))

    def __contains__(self, item: Hashable) -> bool:
        return self.contains(item)

    def clear(self) -> None:
        """Reset the filter."""
        self._bits = bytearray((self._m + 7) // 8)
        self._count = 0

    def __len__(self) -> int:
        return self._count

    def __repr__(self) -> str:
        return (
            f"BloomFilter(n={self._n}, p={self._p}, m={self._m}, "
            f"k={self._k}, size={self._count})"
        )
