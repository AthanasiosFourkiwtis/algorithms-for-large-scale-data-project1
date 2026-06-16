import os
import sys
import random
from fractions import Fraction
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

random.seed(42)
os.makedirs('plots', exist_ok=True)

MAX_C = 22     #gia na min megalonei xwris logo to state space     
MAX_TWO_C = 15      
N_MAX = 1000
c_values = [2, 3, 4, 5]


def next_distribution(dist):
    #dist[C]= pithanotita na vriskomaste sto C
    new_dist = {}
    for C, prob in dist.items():
        p_increase = Fraction(1, 2**C)
        p_stay = Fraction(2**C - 1, 2**C)
        # menw sto idio C
        new_dist[C] = new_dist.get(C, Fraction(0, 1)) + prob * p_stay
        #anevenw sto C+1
        new_C = min(C + 1, MAX_C)
        new_dist[new_C] = new_dist.get(new_C, Fraction(0, 1)) + prob * p_increase

    return new_dist
    
def estimate_from_C(C):
    return Fraction(2**C-1,1)
    
def success_probability(dist, n, c): # gia ayto to n poia h pithanotita i ektimisi na einai anamesa sto n/c kai sto c*n
    low = Fraction(n, c)
    high = Fraction(c * n, 1)
    
    total = Fraction(0, 1) #gia na vrw sto telos tin sinoliki pithanothta

    for C, prob in dist.items():
        estimate = estimate_from_C(C) # metatrepw c se estimate
        if low <= estimate <= high:
            total += prob

    return total

def filter_good_states(dist, n, c):
    low = Fraction(n, c)
    high = Fraction(c * n, 1)

    good = {}
    for C, prob in dist.items():
        estimate = estimate_from_C(C)
        if low <= estimate <= high:
            good[C] = prob

    return good

results_2b = {}

def compute_survival(c,N_MAX=1000):
    survival = {0: Fraction(1, 1)} #arxika C=0 kai profanws den exw apotixei akoma
    probs = []
    for n in range(1, N_MAX + 1):
        survival = next_distribution(survival)
        survival = filter_good_states(survival, n, c)

        total_prob = sum(survival.values(), Fraction(0, 1))#synoliki pithanotita oswn katastasewn eftasan mexri telous
        probs.append(float(total_prob))

    return probs


def next_joint_dist(joint_dist):
    new_dist = {}
    for state in joint_dist:
        c1, c2 = state
        prob_state = joint_dist[state]

        # periptwsh 1: den anevainei kanenas
        p_stay_1 = Fraction(2**c1 - 1, 2**c1)
        p_stay_2 = Fraction(2**c2 - 1, 2**c2)
        new_state = (c1, c2)
        new_prob = prob_state * p_stay_1 * p_stay_2
        new_dist[new_state] = new_dist.get(new_state, Fraction(0, 1)) + new_prob

        # periptwsh 2: anevainei mono o deyteros
        p_up_2 = Fraction(1, 2**c2)
        new_state = (c1, min(c2 + 1, MAX_TWO_C))
        new_prob = prob_state * p_stay_1 * p_up_2
        new_dist[new_state] = new_dist.get(new_state, Fraction(0, 1)) + new_prob

        # periptwsh 3: anevainei mono o protos
        p_up_1 = Fraction(1, 2**c1)
        new_state = (min(c1 + 1, MAX_TWO_C), c2) 
        new_prob = prob_state * p_up_1 * p_stay_2
        new_dist[new_state] = new_dist.get(new_state, Fraction(0, 1)) + new_prob

        # periptwsh 4: anevainoun kai oi 2
        new_state = (min(c1 + 1, MAX_TWO_C), min(c2 + 1, MAX_TWO_C))
        new_prob = prob_state * p_up_1 * p_up_2
        new_dist[new_state] = new_dist.get(new_state, Fraction(0, 1)) + new_prob

    return new_dist
def mean_estimate(c1, c2):
    est1 = 2**c1 - 1
    est2 = 2**c2 - 1
    return Fraction(est1 + est2, 2)


def success_prob_joint(joint_dist, n, c):
    low = Fraction(n, c)
    high = Fraction(c * n, 1)

    total = Fraction(0, 1)

    for state in joint_dist:
        c1, c2 = state
        prob_state = joint_dist[state]

        avg_est = mean_estimate(c1, c2)

        if low <= avg_est <= high:
            total += prob_state

    return total
    
# ── A2α ──────────────────────────────────────────────────────────────────────
print("=== A2α: Exact probability analysis for c ∈ {2,3,4,5} ===")
# arxiki katanomh prin apo inserts eimaste sto C=0
dist = {0: Fraction(1, 1)}
results = {}

for c in c_values:
    results[c]=[]
 # gia kathe n apo 1 ews 1000
for n in range(1, N_MAX + 1):
    dist = next_distribution(dist)
    for c in c_values:
        p=success_probability(dist,n,c)
        results[c].append(p)

#print ths xeiroterhs periptwshsgia kathe c
for c in c_values:
    probs = results[c]
    min_prob = min(probs)
    worst_n = probs.index(min_prob) + 1
    print(f"c={c}: min probability={float(min_prob):.10f}, worst n={worst_n}")


plt.figure(figsize=(12, 6))
ns = list(range(1, N_MAX + 1))

for c in c_values:
    probs = [float(p) for p in results[c]]
    min_prob = min(results[c])
    worst_n = results[c].index(min_prob) + 1
    plt.plot(ns, probs, label=f'c={c} (min={float(min_prob):.10f} at n={worst_n})')

plt.xlabel('n')
plt.ylabel('P(n/c ≤ estimate ≤ c·n)')
plt.title('A2α: Success Probability vs n for Morris Counter (α=2)')
plt.legend()
plt.tight_layout()
plt.savefig('plots/A2a_success_prob.png')
plt.close()
print("Saved plots/A2a_success_prob.png")


# ── A2β ──────────────────────────────────────────────────────────────────────
print("\n=== A2β: Probability of staying in bounds for ALL steps 1..1000 ===")
results_2b = {}
for c in c_values:
    probs_surv = compute_survival(c, N_MAX=N_MAX)
    results_2b[c] = probs_surv
    print(f"c={c}: P(in bounds throughout all {N_MAX} inserts) = {probs_surv[-1]:.10f}")

# ── A2γ ──────────────────────────────────────────────────────────────────────
print("=== A2γ: Two 4-bit Morris counters ===")

joint_dist = {(0, 0): Fraction(1, 1)}
results_2c = {}

for c in c_values:
    results_2c[c] = []

for n in range(1, N_MAX + 1):
    joint_dist = next_joint_dist(joint_dist)

    for c in c_values:
        p = success_prob_joint(joint_dist, n, c)
        results_2c[c].append(float(p))

for c in c_values:
    probs = results_2c[c]
    min_prob = min(probs)
    worst_n = probs.index(min_prob) + 1
    print(f"c={c}: min probability={min_prob:.4f}, worst n={worst_n}")

plt.figure(figsize=(12, 6))
ns = list(range(1, N_MAX + 1))

for c in c_values:
    probs = results_2c[c]
    min_prob = min(probs)
    worst_n = probs.index(min_prob) + 1
    plt.plot(ns, probs, label=f'c={c} (min={min_prob:.4f} at n={worst_n})')

plt.xlabel("n")
plt.ylabel("P(n/c <= mean estimate <= c*n)")
plt.title("A2γ: Two 4-bit Morris Counters")
plt.legend()
plt.tight_layout()
plt.savefig("plots/A2c_two_4bit.png")
plt.close()