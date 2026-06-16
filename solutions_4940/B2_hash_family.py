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
Στο Β2β δεν κάνω πείραμα, αλλά θεωρητική απόδειξη. Η οικογένεια V(2^d)
ορίζεται με affine μετασχηματισμούς πάνω από το GF(2), οπότε κάθε bit
της εξόδου είναι γραμμικός συνδυασμός των bit της εισόδου και μιας σταθεράς.

Επειδή τα bit της εξόδου είναι ομοιόμορφα και ανεξάρτητα, η πιθανότητα
τα πρώτα r bit να είναι όλα μηδέν είναι ακριβώς (1/2)^r.

Έτσι, για δύο διαφορετικά στοιχεία x ≠ y, η πιθανότητα να έχουν και τα δύο
τα πρώτα r bit ίσα με μηδέν είναι (1/4)^r.

Άρα, η οικογένεια V(2^d) ικανοποιεί ακριβώς τις δύο ιδιότητες που χρειάζεται
ο αλγόριθμος Flajolet-Martin.

── B2γ ──────────────────────────────────────────────────────────────────────
Η οικογένεια V(2^d) είναι θεωρητικά καλύτερη, γιατί από το Β2β φαίνεται ότι
ικανοποιεί ακριβώς τις δύο ιδιότητες που χρειάζεται ο αλγόριθμος Flajolet-Martin.
Άρα, για τη V(2^d) έχουμε σωστές θεωρητικές εγγυήσεις.

Αντίθετα, η H(2^d) δεν ικανοποιεί αυτές τις ιδιότητες ακριβώς, αλλά από το Β2α
φαίνεται ότι στην πράξη τις προσεγγίζει αρκετά καλά. Επομένως, η H(2^d) είναι
θεωρητικά πιο αδύναμη, αλλά παραμένει πολύ καλή για πρακτική χρήση.

Το βασικό μειονέκτημα της V(2^d) είναι το κόστος σε χώρο. Για να οριστεί μία
συνάρτηση της οικογένειας V(2^d), χρειάζονται περίπου d(d+1) bits, ενώ για την
H(2^d) χρειάζονται περίπου 2d bits.

Άρα, όταν το d μεγαλώνει, η V(2^d) γίνεται πολύ πιο ακριβή ως προς τον χώρο.
Για μικρές τιμές, όπως d = 20, και οι δύο οικογένειες μπορούν να χρησιμοποιηθούν.
Όμως για μεγαλύτερες τιμές, όπως d = 100, η V(2^d) γίνεται αρκετά βαριά, ενώ
η H(2^d) παραμένει πιο πρακτική.

Συμπερασματικά, η V(2^d) είναι καλύτερη από θεωρητικής πλευράς, ενώ η H(2^d)
είναι πιο πρακτική και πιο οικονομική σε χώρο. Για αυτό, στην πράξη συχνά
προτιμάται η H(2^d), παρόλο που δεν δίνει ακριβώς τις ίδιες θεωρητικές εγγυήσεις.
""")