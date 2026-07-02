# Algorithms for Large-Scale Data — Project 1

First assignment for the Algorithms for Large-Scale Data course (Department of Computer Science & Engineering, University of Ioannina).

The code implements several streaming algorithms and runs experiments that output charts into the `plots/` folder.

## Files (`solutions_4940/`)

- `A1_morris_counter.py` — Morris counter
- `A2_morris_exact.py` — exact computation of the Morris counter's distribution
- `B1_distinct_counting.py` — distinct-element counting (trailing zeros, Trie)
- `B2_hash_family.py` — hash family
- `B3_bjkst.py` — BJKST algorithm
- `C1_bloom_intersection.py` — Bloom filters and set intersection
- `D_packet_tracing.py` — packet tracing with Bloom filters
- `run_all.py` — runs all of the above
- `graph*.txt` — input data
- `plots/` — the generated charts

## Usage

Requires Python 3 and matplotlib:

```bash
pip install matplotlib
cd solutions_4940
python run_all.py
```

To run a single exercise, e.g.:

```bash
python B3_bjkst.py
```

Every script sets `random.seed(42)`, so the results are identical on every run.

## Other files

- `report_final.pdf` — the project report
- `Assignment Sheet 1.pdf` — the assignment handout

## Author

Athanasios Fourkiotis
