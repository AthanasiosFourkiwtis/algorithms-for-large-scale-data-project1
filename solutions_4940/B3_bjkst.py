import random
import math
import os
import heapq
import matplotlib.pyplot as plt

random.seed(42)
os.makedirs("plots", exist_ok=True)

# oi statheres tis ekfwnhshs
m = 2**20
M = m**3

q = 1048583
p = q**3

def make_hash():
    a = random.randint(1, p - 1)
    b = random.randint(0, p - 1)

    def h(x):
        return (((a * x + b) % p) % M) + 1

    return h


class TopKSmallest:
    def __init__(self, k):
        self.k = k
        self.heap = []     # tha krataei arnitikes times gia na to xrisimopoihsoume ws max-heap
        self.values = set()

    def add(self, v):
        # den theloume duplicates
        if v in self.values:
            return

        # an den exei gemisei akoma, bale to
        if len(self.heap) < self.k:
            heapq.heappush(self.heap, -v)
            self.values.add(v)
            return

        # to megalutero apo ta k mikrotera einai stin korifi
        current_biggest = -self.heap[0]

        # an to neo v einai mikrotero, tote prepei na mpei mesa
        if v < current_biggest:
            removed = -heapq.heapreplace(self.heap, -v)
            self.values.remove(removed)
            self.values.add(v)

    def kth_smallest(self):
        if len(self.heap) < self.k:
            return None
        return -self.heap[0]


class BJKST:
    def __init__(self, eps):
        self.eps = eps
        self.t = math.ceil(96 / (eps ** 2))
        self.h = make_hash()
        self.smallest_hashes = TopKSmallest(self.t)

    def insert(self, x):
        x=x+1
        hx = self.h(x)
        self.smallest_hashes.add(hx)

    def query(self):
        v = self.smallest_hashes.kth_smallest()

        if v is None:
            return 0

        return (self.t * M) / v


def generate_uniform(d=20):
    return random.randint(0, 2**d - 1)


def generate_nonuniform():
    x = 0

    # bits 1-5
    for i in range(5):
        if random.random() < 0.5:
            x |= (1 << (19 - i))

    # bits 6-10
    for i in range(5):
        if random.random() < 0.25:
            x |= (1 << (14 - i))

    # bits 11-15
    for i in range(5):
        if random.random() < 0.125:
            x |= (1 << (9 - i))

    # bits 16-20
    for i in range(5):
        if random.random() < 0.0625:
            x |= (1 << (4 - i))

    return x


def run_bjkst_experiment(eps, gen_fn, dist_name, plot_filename, n=1_000_000):
    print(f"\n=== B3α: BJKST, eps={eps}, distribution={dist_name} ===")

    bjkst = BJKST(eps)
    real_seen = set()

    x_values = []
    real_values = []
    est_values = []

    for i in range(1, n + 1):
        x = gen_fn()
        real_seen.add(x)
        bjkst.insert(x)

        real_distinct = len(real_seen)

        # krataw dedomena gia plot mono otan exw toulaxiston t distinct
        if i % 50000 == 0 and real_distinct >= bjkst.t:
            estimate = bjkst.query()

            x_values.append(i)
            real_values.append(real_distinct)
            est_values.append(estimate)

            print(i, real_distinct, estimate)

    plt.figure(figsize=(12, 5))
    plt.plot(x_values, real_values, label="True distinct", alpha=0.8)
    plt.plot(x_values, est_values, label=f"BJKST estimate (eps={eps})", alpha=0.8)
    plt.xlabel("n (inserts)")
    plt.ylabel("Distinct count")
    plt.title(f"B3α: BJKST on {dist_name} distribution")
    plt.legend()
    plt.tight_layout()
    plt.savefig(plot_filename)
    plt.close()

    print(f"Saved {plot_filename}")


# paradeigmata runs
run_bjkst_experiment(0.1, generate_uniform, "uniform", "plots/B3_uniform_eps01.png")
run_bjkst_experiment(0.05, generate_uniform, "uniform", "plots/B3_uniform_eps005.png")
run_bjkst_experiment(0.1, generate_nonuniform, "non-uniform", "plots/B3_nonuniform_eps01.png")
run_bjkst_experiment(0.05, generate_nonuniform, "non-uniform", "plots/B3_nonuniform_eps005.png")

# ── B3β ──────────────────────────────────────────────────────────────────────
print("\n=== B3β: Median trick for success probability ≥ 99.9% ===")

delta = 0.001
K_real = 18 * math.log(1 / delta)
K = math.ceil(K_real)

print("delta =", delta)
print("K real =", K_real)
print("K =", K)
print("Failure bound =", math.exp(-K / 18))
print("Success probability >=", 1 - math.exp(-K / 18))


def median_trick_estimate(eps, gen_fn, n=1_000_000):
    estimates = []

    for _ in range(K):
        bjkst = BJKST(eps)
        for _ in range(n):
            x = gen_fn()
            bjkst.insert(x)
        estimates.append(bjkst.query())

    estimates.sort()
    return estimates[len(estimates) // 2]


print("\nMedian trick example:")
est_med = median_trick_estimate(0.1, generate_uniform, n=200000)
print("Median estimate for eps=0.1 on uniform data =", est_med)