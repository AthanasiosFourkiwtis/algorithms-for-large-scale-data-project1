import random
import math
import os                     #gia ton fakelo pou tha apothikevw ta plots
import sys
import matplotlib              #gia na sxediazw to kathe plot

matplotlib.use('Agg')           #gia na swsw to plot se arxeio
import matplotlib.pyplot as plt

random.seed(42)                       # gia kathe run na pairnw thn idia seira random arithmwn oste to plot na vgenei idio an to ksanakanw run
os.makedirs('plots', exist_ok=True)   #dhmiourgw fakelo plots an den yparxei idi

def morris_insert(C, alpha=2.0):
    pithanotita = 1.0 / (alpha ** C)
    if random.random() < pithanotita: 
        return C + 1
    return C
    
    
def morris_query(C, alpha=2.0):
    if alpha == 2.0:
        return (2.0 ** C) - 1.0
    return (1.0 / (alpha - 1.0)) * ((alpha ** C) - 1.0)


# ── A1α ──────────────────────────────────────────────────────────────────────
print("=== A1α: Morris Counter α=2, n=1,000,000 ===")
n = 1_000_000
alpha = 2.0
C = 0
x_values = [] #gia to grafima
y_values = [] #gia ti grafima
for i in range(1, n + 1):
    C = morris_insert(C, alpha)
    ektimisi = morris_query(C, alpha)
    print(f"{i}: {ektimisi:.0f}")
    if i % 10_000 == 0:
        x_values.append(i)
        y_values.append(ektimisi)
    if i % 100_000 == 0:
        sys.stdout.flush()

plt.figure(figsize=(10, 5))
plt.step(x_values, y_values, where='post', color='steelblue')
plt.xlabel('n')
plt.ylabel('Estimate')
plt.title('A1α: Morris Counter Estimate vs n (α=2)')
plt.tight_layout()
plt.savefig('plots/A1a_morris.png')
plt.close()
print("Saved plots/A1a_morris.png")

# ── A1β ──────────────────────────────────────────────────────────────────────
print("\n======== A1β: 5 independent Morris counters, mean & median ===========")
import statistics # gia tin diameso

n = 1_000_000
alpha = 2.0
counters = [0, 0, 0, 0, 0] 
x_values_b = []
mesos_oros_b = []
diamesos_b = []

for i in range(1, n + 1):
    new_counters=[]
    
    for c in counters:
        new_counters.append(morris_insert(c))
        
        
    counters=new_counters
    estimates=[]
    for c in counters:
        estimates.append(morris_query(c))
    
    mesos_oros_est = sum(estimates) / 5
    diamesos_est = statistics.median(estimates)
    print(i, mesos_oros_est, diamesos_est)
    
    if i % 10_000 == 0:  #kratima shmeiwn gia plot gia kathe 10.000 vimata 
        x_values_b.append(i)
        mesos_oros_b.append(mesos_oros_est)
        diamesos_b.append(diamesos_est)

plt.figure(figsize=(10, 5))
plt.plot(x_values_b, mesos_oros_b, label='Mean')
plt.plot(x_values_b, diamesos_b, label='Median')
plt.xlabel('n')
plt.ylabel('Estimate')
plt.title('"5 Morris counters"')
plt.legend()
plt.tight_layout()
plt.savefig('plots/A1b_mean_median.png')
plt.close()
print("Saved plots/A1b_mean_median.png")

# ── A1γ ──────────────────────────────────────────────────────────────────────
print("\n=== A1γ: Memory analysis ===")

def bits_for_direct(n):
    return math.ceil(math.log2(n + 1))

def bits_for_5_morris(n):
    c_approx = math.ceil(math.log2(n))     # giati gia a=2 isxyei C ≈ log2(n)
    bits_one = math.ceil(math.log2(c_approx + 1))
    return 5 * bits_one, c_approx, bits_one

values = [1_000_000, 10_000_000, 33_554_432, 100_000_000, 1_000_000_000]

for n in values:
    morris_bits, c_approx, bits_one = bits_for_5_morris(n)
    direct_bits = bits_for_direct(n)

    if morris_bits < direct_bits:
        result = "worthwhile"
    else:
        result = "not worthwhile"

    print(f"n={n}")
    print(f"approx C = {c_approx}")
    print(f"bits for one Morris counter = {bits_one}")
    print(f"bits for 5 Morris counters = {morris_bits}")
    print(f"bits for direct counter = {direct_bits}")
    print(f"result: {result}")

# ── A1δ ──────────────────────────────────────────────────────────────────────
print("\n=== A1δ: 8-bit Morris counters with different α values ===")
n = 1_000_000
max_c = 255  # 8 bits ara mporw na apothikevw times apo 0 ews 255
alphas = [1.02, 1.0427, 1.5, 2.0, 3.0]

plt.figure(figsize=(12, 6))
for alpha in alphas:
    C = 0
    x_values = []
    y_values = []

    for i in range(1, n + 1):
        p = 1 / (alpha ** C)

        if C < max_c and random.random() < p:
            C += 1

        estimate = morris_query(C, alpha)

        if i % 10000 == 0:
            x_values.append(i)
            y_values.append(estimate)

    plt.plot(x_values, y_values, label=f"α={alpha}")
plt.axhline(1_000_000, linestyle="--", label="true n")
plt.xlabel("n")
plt.ylabel("Estimate")
plt.title("A1δ: 8-bit Morris Counter with Different α Values")
plt.legend()
plt.tight_layout()
plt.savefig("plots/A1d_8bit.png")
plt.close()

# ── A1ε ──────────────────────────────────────────────────────────────────────
print("\n=== A1ε: 15-bit budget, Monte Carlo comparison ===")

alpha_target = 1_000_000 ** (1.0 / 31) # sto algo2 exw 3 morris counter me ton kathena na ftanei mexri to 2^5-1=31 

n_epanalipseis = 500
n_inserts = 1_000_000
target_low= 800_000
target_high = 1_200_000

def run_algo1(n): #Enas Morris counter α=2, 15 bits (C ≤ 32767).
    C = 0
    max_C = 32767  # o eswterinos counter ftanei mexri ton arithmo2^15-1=32767 
    for x in range(n):
        if random.random() < 1.0 / (2.0 ** C):
            C = min(C + 1, max_C) #gia na ayksanw to c kata 1 an petyxei h pithanothta alla na mhn pernaei to c_max
    return morris_query(C, 2.0) #gia na metatrepsw to c se ektimisi

def run_algo2(n, alpha): #3 Morris counters, 5-bit o kathenas (C ≤ 31) o max_c=31
    Counters = [0, 0, 0]
    max_c = 31
    for y in range(n): 
        for j in range(3):  # gia kathe eisagwgh enhmerwnw kai tous 3 morris counters
            if random.random() < 1.0 / (alpha ** Counters[j]):
                Counters[j] = min(Counters[j] + 1, max_c) #ayksanw τον Cs[j] κατά 1 alla oxi panw apo to 31
    e1 = morris_query(Counters[0], alpha)
    e2 = morris_query(Counters[1], alpha)
    e3 = morris_query(Counters[2], alpha)

    return (e1 + e2 + e3) / 3
    
#gia thn algo2 poio a doulevei kalitera se sxesi me ta ypolloipa
alpha_candidates = [2.5, 2.7, alpha_target, 3.0, 3.5]
print("  Selecting best α for Algo2 (50 trials each):")
best_alpha2 = None
best_success_rate2 = -1
for a in alpha_candidates:
    successes = 0
    for t in range(50):
        teliki_ektimisi = run_algo2(n_inserts, a)
        if target_low <= teliki_ektimisi <= target_high:
            successes += 1
    pososto= successes / 50
    if pososto > best_success_rate2:
        best_success_rate2 = pososto
        best_alpha2 = a
print(f"  Selected α={best_alpha2:.4f} for Algo2")

# Monte Carlo gia sygkrisi poio apo algo1 h algo2 exei kaliteri ektimisi
successes_algo1 = []
successes_algo2 = []
for t in range(n_epanalipseis):
    est1 = run_algo1(n_inserts)
    ok1 = target_low <= est1 <= target_high
    successes_algo1.append(ok1)
    
    est2 = run_algo2(n_inserts, best_alpha2)
    ok2 = target_low <= est2 <= target_high
    successes_algo2.append(ok2)
    
    if (t + 1) % 50 == 0:
        print(f"  Trial {t+1}: Algo1 running rate={sum(successes_algo1)/(t+1):.3f}, Algo2={sum(successes_algo2)/(t+1):.3f}")
        sys.stdout.flush()

xs_mc = list(range(1, n_epanalipseis + 1))
conv1 = [sum(successes_algo1[:i]) / i for i in range(1, n_epanalipseis + 1)]
conv2 = [sum(successes_algo2[:i]) / i for i in range(1, n_epanalipseis + 1)]

plt.figure(figsize=(10, 5))
plt.plot(xs_mc, conv1, label='Algo1: single 15-bit counter (α=2)', alpha=0.8)
plt.plot(xs_mc, conv2, label=f'Algo2: 3×5-bit counters (α={best_alpha2:.2f})', alpha=0.8)
plt.axhline(y=0.8, color='gray', linestyle='--', alpha=0.5, label='80% threshold')
plt.xlabel('Number of trials')
plt.ylabel('Success rate P(800K ≤ estimate ≤ 1.2M)')
plt.title('A1ε: Monte Carlo — 15-bit budget')
plt.legend()
plt.tight_layout()
plt.savefig('plots/A1e_monte_carlo.png')
plt.close()
print("Saved plots/A1e_monte_carlo.png")
print(f"\nFinal success rates:")
print(f"  Algo1 (single 15-bit, α=2): {conv1[-1]:.3%}")
print(f"  Algo2 (3×5-bit, α={best_alpha2:.2f}): {conv2[-1]:.3%}")
