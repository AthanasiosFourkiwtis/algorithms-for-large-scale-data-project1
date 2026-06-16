import random
import math
import os
import sys
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

random.seed(42)
os.makedirs('plots', exist_ok=True)

def trailing_zeros(x): #Gia na parw kathe distinct stoixeio kai koitaw posa mhdenika exei sto telos tis diadikhs anaparastashs.
    if x == 0: # gia tin periptwsh dhadh to 0
        return 20 # afou doulevw me 20bitous arithmous
    count = 0
    while (x & 1) == 0: # elegxw to teleutaio bit
        count += 1
        x >>= 1 # gia deksia metatopisi. afou vrika 0 paw sthn dipla thesi
    return count

# -------Trie--------------------------------------------------------
class TrieNode:
    def __init__(self):
        self.children = [None, None] # 2 paidia ena gia bit0 kai ena gia bit1
        self.is_end = False # flag gia na vlepw an teleiwnei enas arithmos ta bits tou dhladh

class Trie:
    def __init__(self, bits):
        self.root = TrieNode() # ftiaxnw tin riza
        self.bits = bits # apothikevw t mhkos twn bits twn arithmwn edw 20
        self.count = 0 # counter gia metrima plhthos diaforetikwn stoixeiwn

    def insert(self, x):
        node=self.root  # ksekinaw apo tin riza
        
        for i in range(self.bits - 1, -1, -1):  # pernaw ola ta bits apo to pio shmantiko pros to ligotero
            bits = (x >> i) & 1 # pairnw to i-osto bit tou arithmou x 
            
            if node.children[bits] is None:
                node.children[bits] = TrieNode() # an gia ayto to padi den exw bit to ftiaxnw
            node = node.children[bits] # paw sto epomeno epipedo tou Trie
            
        if node.is_end == False: # elegxw gia diples isagoges
            node.is_end = True # afou elegksa thn monadikotita twra kanw true to flag oti teliwse edw o apothikeumenos arithmos
            self.count += 1 # distinct count +1
            return True  #afou mpike neo stoixeio
        return False  # an yparxei o arithmos idi mesa den ayksanw to count

# ── B1α ──────────────────────────────────────────────────────────────────────
# ---------------- B1a: FM + Trie ----------------
print("=== B1α: Flajolet-Martin on uniform distribution ===")

d = 20
n = 1_000_000

trie = Trie(d)
R = 0

x_points = []
real_values = []
fm_values = []

for i in range(1, n + 1):
    x = random.randint(0, 2**d - 1)
    trie.insert(x)
    r = trailing_zeros(x)

    if r > R:
        R = r

    estimate = 2 ** R
    real_distinct = trie.count

    print(i, real_distinct, estimate)

    if i % 10000 == 0:
        x_points.append(i)
        real_values.append(real_distinct)
        fm_values.append(estimate)

# plot
plt.figure(figsize=(12, 5))
plt.plot(x_points, real_values, label="True distinct", alpha=0.8)
plt.step(x_points, fm_values, where="post", label="FM Estimate (2^R)", alpha=0.8)

plt.xlabel("n (inserts)")
plt.ylabel("Distinct count")
plt.title("B1α: Flajolet-Martin on Uniform Distribution")
plt.legend()
plt.tight_layout()
plt.savefig("plots/B1a_distinct.png")
plt.close()

print("Saved plots/B1a_distinct.png")

# ── B1β ──────────────────────────────────────────────────────────────────────
print("\n=== B1β: Flajolet-Martin on non-uniform distribution ===")

def generate_nonuniform():
    x = 0
    
    for i in range(5):    # bits 1-5 (MSB)
        if random.random() < 0.5: # ta prwta bits exoun pithanothta 0.5 na ginoun 1
            x |= (1 << (19 - i)) # vazw to 19-i iso me 1
            
    for i in range(5):    # bits 6-10
        if random.random() < 0.25: # ta prwta bits exoun pithanothta 0.25 na ginoun 1
            x |= (1 << (14 - i)) # vazw to 14-i iso me 1
            
    for i in range(5):    # bits 11-15
        if random.random() < 0.125: # ta prwta bits exoun pithanothta 0.125 na ginoun 1
            x |= (1 << (9 - i)) # vazw to 9-i iso me 1
            
    for i in range(5):    # bits 16-20 (LSB)
        if random.random() < 0.0625: # ta prwta bits exoun pithanothta 0.0625 na ginoun 1
            x |= (1 << (4 - i)) # vazw to 4-i iso me 1
            
    return x

print("--- Part 1: Without hash ---")

R_nohash = 0 # megisto trailing zeros 
trie_nohash = Trie(d) # gia pragmatiko distinct count

x_values_nohash = []
real_values_nohash = []
fm_values_nohash = []

for i in range(1, n + 1):
    x = generate_nonuniform()

    trie_nohash.insert(x)

    r = trailing_zeros(x) # gia na vrw trailing zeros panw sto idio to x dhladh h(x)=x
    if r > R_nohash:
        R_nohash = r

    estimate = 2 ** R_nohash
    real_distinct = trie_nohash.count

    if i % 10000 == 0: # kathe 10k vimata krataw shmeia gia to plot
        x_values_nohash.append(i)
        real_values_nohash.append(real_distinct)
        fm_values_nohash.append(estimate)
        print(i, real_distinct, estimate)

plt.figure(figsize=(12, 5))
plt.plot(x_values_nohash, real_values_nohash, label="True distinct", alpha=0.8)
plt.step(x_values_nohash, fm_values_nohash, where="post", label="FM Estimate (no hash)", alpha=0.8)
plt.xlabel("n (inserts)")
plt.ylabel("Distinct count")
plt.title("B1β Part 1: FM on Non-Uniform Distribution (no hash)")
plt.legend()
plt.tight_layout()
plt.savefig("plots/B1b_nonuniform.png")
plt.close()

print("Saved plots/B1b_nonuniform.png")


# ---------- Part 2: me hash ----------
print("\n--- Part 2: With hash ---")

p = 1048583 # arithmos > tou 2**20
a = random.randint(1, p - 1)
b = random.randint(0, p - 1)

def my_hash(x):
    return ((a * x + b) % p) % (2 ** d)

R_hash = 0
trie_hash = Trie(d)

x_values_hash = []
real_values_hash = []
fm_values_hash = []

for i in range(1, n + 1):
    x = generate_nonuniform()

    trie_hash.insert(x)

    hx = my_hash(x)
    r = trailing_zeros(hx)

    if r > R_hash:
        R_hash = r

    estimate = 2 ** R_hash
    real_distinct = trie_hash.count

    if i % 10000 == 0:
        x_values_hash.append(i)
        real_values_hash.append(real_distinct)
        fm_values_hash.append(estimate)
        print(i, real_distinct, estimate)

plt.figure(figsize=(12, 5))
plt.plot(x_values_hash, real_values_hash, label="True distinct", alpha=0.8)
plt.step(x_values_hash, fm_values_hash, where="post", label="FM Estimate (with hash)", alpha=0.8)
plt.xlabel("n (inserts)")
plt.ylabel("Distinct count")
plt.title("B1β Part 2: FM on Non-Uniform Distribution (with hash)")
plt.legend()
plt.tight_layout()
plt.savefig("plots/B1b_with_hash.png")
plt.close()

print("Saved plots/B1b_with_hash.png")