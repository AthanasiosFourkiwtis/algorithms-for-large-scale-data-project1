# Algorithms for Large-Scale Data — Project 1

First project for the Algorithms for Large-Scale Data course (CSE, University of Ioannina).

The code implements a bunch of streaming algorithms and runs experiments that put charts in the `plots/` folder.

## Files (`solutions_4940/`)

- `A1_morris_counter.py` — Morris counter
- `A2_morris_exact.py` — exact computation of the Morris counter's distribution
- `B1_distinct_counting.py` — counting distinct elements (trailing zeros, Trie)
- `B2_hash_family.py` — hash family
- `B3_bjkst.py` — the BJKST algorithm
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
