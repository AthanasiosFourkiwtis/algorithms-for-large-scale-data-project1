# Algorithms for Large-Scale Data — Project 1

First project for the Algorithms for Large-Scale Data course (CSE, University of Ioannina).

## What the assignment asks

The general theme is streaming algorithms: how do you answer questions about huge data streams when you can't afford to store everything? The project has four parts:

- **A — Morris counter.** Count events approximately using only a handful of bits: instead of counting every event, you increment a small counter with probability that drops as the counter grows, and the estimate is `2^C - 1`. The assignment asks to implement it, study its distribution both experimentally and *exactly* (computing the actual probabilities, not just simulating), and compare tricks like averaging multiple counters or splitting a bit budget across counters.
- **B — Counting distinct elements.** Implement Flajolet-Martin style distinct counting with trailing zeros, look into what properties the hash family needs (and prove that one family has them), and implement BJKST with the median trick to push the success probability up to 99.9%.
- **C — Bloom filters.** Use Bloom filters to approximate a set intersection without storing the sets.
- **D — Packet tracing.** Every router in a network keeps a Bloom filter of the messages that passed through it. Given a message at the destination, trace it *backwards* through the network to find which source sent it, and study how the graph shape and the number of hash functions affect the success rate.

## How I solved it

**A.** For the exact analysis (A2) I don't simulate — I keep the full probability distribution over the counter values and update it step by step, so the numbers are exact. For the bit-budget question (A1ε) I compare a single 15-bit Morris counter against three 5-bit counters (with a tuned α) using Monte Carlo, and pick α for the second scheme by trying values and keeping the one with the smallest error.

**B.** The distinct counting uses the trailing-zeros idea: hash every element and remember the maximum number of trailing zeros R seen; the estimate is 2^R. It works only if the hash spreads elements uniformly and pairwise-independently, which is exactly what B2 is about: for V(2^d) (affine maps over GF(2)) those properties can be proven, while H(2^d) only satisfies them approximately — but experimentally it comes close and is much cheaper in space (~2d bits vs ~d² bits per function). BJKST (B3) keeps a sample of the smallest hash values instead of just one maximum, which makes the estimate much more stable, and running several copies and taking the median pushes the failure probability down exponentially.

**D.** For the simulation, each message picks a random path from a random source to the sink, and gets inserted into the Bloom filter of every router on the way. The reverse trace starts from the sink and follows backwards only the routers whose filter claims to contain the message; the trace counts as successful when the only source it reaches is the real one. False positives make the search leak into wrong branches, so graphs with short paths and few branches trace better, and the number of hash functions k has a sweet spot (theory says k = (N/n)·ln2) — too few hashes means a high false-positive rate, too many fill the filter up. I find the best k experimentally per graph.

## Files (`solutions_4940/`)

- `A1_morris_counter.py` — Morris counter
- `A2_morris_exact.py` — exact computation of the Morris counter's distribution
- `B1_distinct_counting.py` — counting distinct elements (trailing zeros)
- `B2_hash_family.py` — hash family properties (experiment + proof)
- `B3_bjkst.py` — the BJKST algorithm + median trick
- `C1_bloom_intersection.py` — Bloom filters and set intersection
- `D_packet_tracing.py` — packet tracing with Bloom filters
- `run_all.py` — runs all of the above
- `graph*.txt` — input data
- `plots/` — the charts that get generated

## How to run

You need Python 3 and matplotlib:

```bash
pip install matplotlib
cd solutions_4940
python run_all.py
```

To run just one exercise, e.g.:

```bash
python B3_bjkst.py
```

All the scripts have `random.seed(42)`, so they give the same results every time.

## Other files

- `report_final.pdf` — my report
- `Assignment Sheet 1.pdf` — the assignment description

## Author

Athanasios Fourkiotis
