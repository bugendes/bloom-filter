# Bloom Filter

A space-efficient probabilistic data structure that answers "is this element in the set?" with no false negatives and a tunable false positive rate.

## How It Works

A bloom filter uses:
1. A **bit array** of `m` bits (all initially 0).
2. `k` **independent hash functions**, each mapping an element to a position in the array.

**Add:** Hash the element with all k functions, set all k corresponding bits to 1.

**Query:** Hash with all k functions. If ALL k bits are 1, return "probably present." If any bit is 0, return "definitely absent."

Because multiple elements may hash to the same bits, false positives occur (a query returns "probably present" for an element never added). But false negatives are impossible — if an element was added, all its bits are 1.

### Optimal Parameters

Given expected insertions `n` and desired false positive rate `p`:

- **Bit array size:** `m = -n·ln(p) / (ln2)²`
- **Hash functions:** `k = (m/n) · ln2`

This implementation uses double hashing (Kirsch-Mitzenmacker) to simulate k hash functions from two hash computations (MD5 + SHA-256).

## Complexity

| Operation | Time | Space |
|-----------|------|-------|
| add       | O(k) | —     |
| contains  | O(k) | —     |

Space: O(m) bits total, O(1) per element amortized (far less than storing the elements themselves).

## Applications

**Databases:** Cassandra, HBase, and PostgreSQL use bloom filters to avoid unnecessary disk reads. If the filter says "not in this SSTable," skip it entirely.

**Web Crawlers:** Check if a URL has been visited without storing all URLs. A crawler visiting 1 billion pages with 1% FP rate needs only ~1.2 GB.

**Email Spam:** Check incoming addresses against a bloom filter of known spammers — O(1) lookup with negligible memory.

**Bioinformatics:** Sequence alignment tools (BLAT, BWA) use bloom filters to index k-mers, reducing memory by 10-20× compared to hash sets.

**Network Routers:** Packet deduplication and content-based routing use bloom filters for line-rate membership testing.
