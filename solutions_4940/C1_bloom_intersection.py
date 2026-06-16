import random
import matplotlib.pyplot as plt

random.seed(42)

# ---------------- Bloom Filter ----------------
p = 1048583

def split_100bit_string(s):
    parts = []
    for i in range(0, 100, 20):
        parts.append(int(s[i:i+20], 2))
    return parts

def make_bloom_hash():
    a = random.randint(1, p - 1)
    b = random.randint(0, p - 1)

    def h(s):
        c = 0
        for part in split_100bit_string(s):
            c = (a * (part + c) + b) % p
        return c

    return h



class BloomFilter:
    def __init__(self, m, k):
        self.m = m
        self.k = k
        self.bits = [0] * m
        self.hashes = [make_bloom_hash() for _ in range(k)]

    def positions(self, item):
        pos = []
        for h in self.hashes:
            pos.append(h(item) % self.m)
        return pos
    def add(self, item):
        for p in self.positions(item):
            self.bits[p] = 1

    def contains(self, item):
        for p in self.positions(item):
            if self.bits[p] == 0:
                return False
        return True

# ---------------- Dimiourgia arxeiwn ----------------

def make_random_file():
    # 100-bit arxeio ws string
    s = ""
    for _ in range(100):
        s += random.choice(["0", "1"])
    return s


def make_data():
    common = set()

    while len(common) < 10:
        common.add(make_random_file())

    A = set(common)
    B = set(common)

    while len(A) < 100000:
        x = make_random_file()
        if x not in B:
            A.add(x)

    while len(B) < 100000:
        x = make_random_file()
        if x not in A:
            B.add(x)

    return A, B, common


# ---------------- Ena gyros protokollou ----------------

def one_round(sender_set, receiver_candidates, m, k):
    bf = BloomFilter(m, k)

    for item in sender_set:
        bf.add(item)

    new_candidates = set()

    for item in receiver_candidates:
        if bf.contains(item):
            new_candidates.add(item)

    communication = m   # steilame m bits tou bloom filter
    return new_candidates, communication


# ---------------- Protokollo pollwn gyrwn ----------------

def run_protocol(A, B, rounds, k, mode="fixed"):
    candidates_A = set(A)
    candidates_B = set(B)

    total_communication = 0
    last_B_positives = set(B)

    for r in range(rounds):
        if r % 2 == 0:
            # A -> B
            if mode == "fixed":
                m = 500000
            else:
                m = max(10, 5 * len(candidates_A))

            candidates_B, comm = one_round(candidates_A, candidates_B, m, k)
            total_communication += comm

            # kratame auto pou vrike o B sto teleutaio filter tou A
            last_B_positives = set(candidates_B)

        else:
            # B -> A
            if mode == "fixed":
                m = 500000
            else:
                m = max(10, 5 * len(candidates_B))

            candidates_A, comm = one_round(candidates_B, candidates_A, m, k)
            total_communication += comm

    count = len(last_B_positives)
    return last_B_positives, count, total_communication


# ---------------- Peirama ----------------

A, B, common = make_data()

results = []

for mode in ["fixed", "dynamic"]:
    for rounds in [1, 2, 3, 4, 5]:
        for k in [1, 2, 3, 5, 10]:
            last_B_positives, count, total_comm = run_protocol(A, B, rounds, k, mode)

            all_common_found = common.issubset(last_B_positives)

            results.append((mode, rounds, k, count, total_comm, all_common_found))

            print("mode =", mode,
                  "rounds =", rounds,
                  "k =", k,
                  "count =", count,
                  "communication =", total_comm,
                  "all common found =", all_common_found)


# ---------------- Plot ----------------
xs = []
ys = []

for mode, rounds, k, count, total_comm, ok in results:
    if ok:
        xs.append(f"{mode[:3]}-{rounds}r-{k}k")
        ys.append(count)

plt.figure(figsize=(14, 6))
plt.bar(xs, ys)
plt.xticks(rotation=60)
plt.xlabel("setting")
plt.ylabel("count")
plt.title("Γ1α: Bloom filter intersection (count for B on last filter from A)")
plt.tight_layout()
plt.savefig("plots/G1a_bloom_intersection.png")
plt.close()

print("Saved plots/G1a_bloom_intersection.png")

