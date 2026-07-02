import random
import math
import os
import sys
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

random.seed(42)
os.makedirs('plots', exist_ok=True)

d = 20
p = 1048583  # arithmos ligo > apo 2**20
n_samples=20000 #Oso megalitero toso pio stathero to observed apotelesma

def trailing_zeros(x):
    if x == 0:
        return d
    count = 0
    while (x & 1) == 0:
        count += 1
        x >>= 1
    return count

def h_hash(x, alpha, beta):
    return ((alpha * x + beta) % p) % (2**d)

# ── B2α ──────────────────────────────────────────────────────────────────────
print("=== B2α: Empirically check H(2^d) properties ===")
r_values_test = [1, 2, 3, 4, 5]
x_values = [0, 1, 42, 1000, 2**10, 2**15, 2**20 - 1] 
xy_pairs = [(0, 1), (1, 2), (42, 137), (1000, 2000), (2**10, 2**10 + 1)]

# -------- Property 1 --------
print("\nProperty 1: P(tr(h(x)) >= r) ~ 1/2^r")
for x in [0, 1, 42, 1000]:# Prepei thewritina na einai peripou 1/(2^r)
    for r in [1, 2, 3, 4]:
        success = 0
        for i in range(n_samples):
            alpha = random.randint(1, p - 1)
            beta = random.randint(0, p - 1)
            
            hx = h_hash(x, alpha, beta)
            if trailing_zeros(hx) >= r:
                success += 1
        observed = success / n_samples
        expected = 1.0 / (2**r)
        print(f"r={r}: observed={observed:.4f}, expected={expected:.4f}")

# -------- Property 2 --------
print("\nProperty 2: P(tr(h(x)) >= r and tr(h(y)) >= r) ~ 1/4^r")
for (x, y) in [(1, 2), (42, 137), (1000, 2000)]: # Prepei thewritina na einai peripou 1/(4^r)
    for r in [1, 2, 3]:
        success = 0
        for k in range(n_samples):
            alpha = random.randint(1, p - 1)
            beta = random.randint(0, p - 1)
            hx = h_hash(x, alpha, beta)
            hy = h_hash(y, alpha, beta)
            
            if trailing_zeros(hx) >= r and trailing_zeros(hy) >= r:
                success += 1
        observed = success / n_samples
        expected = 1.0 / (4**r)
        
        print(f"r={r}: observed={observed:.4f}, expected={expected:.4f}")
print("""── B2β ──────────────────────────────────────────────────────────────────────
B2β is not an experiment but a theoretical proof. The family V(2^d)
is defined through affine transformations over GF(2), so every output
bit is a linear combination of the input bits and a constant.

Since the output bits are uniform and independent, the probability
that the first r bits are all zero is exactly (1/2)^r.

Hence, for two distinct elements x ≠ y, the probability that both
have their first r bits equal to zero is (1/4)^r.

Therefore the family V(2^d) satisfies exactly the two properties the
Flajolet-Martin algorithm requires.

── B2γ ──────────────────────────────────────────────────────────────────────
The family V(2^d) is theoretically better, since B2β shows that it
satisfies exactly the two properties the Flajolet-Martin algorithm requires.
So V(2^d) comes with proper theoretical guarantees.

By contrast, H(2^d) does not satisfy these properties exactly, but B2α
shows that in practice it approximates them quite well. H(2^d) is therefore
theoretically weaker, yet remains very good for practical use.

The main drawback of V(2^d) is its space cost. Defining one function
of the family V(2^d) takes roughly d(d+1) bits, whereas one from
H(2^d) takes roughly 2d bits.

So as d grows, V(2^d) becomes far more expensive in space.
For small values, such as d = 20, either family is usable.
But for larger values, such as d = 100, V(2^d) gets quite heavy, while
H(2^d) stays more practical.

In summary, V(2^d) is better from a theoretical standpoint, while H(2^d)
is more practical and more space-efficient. That is why in practice H(2^d)
is often preferred, even though it does not give exactly the same theoretical guarantees.
""")