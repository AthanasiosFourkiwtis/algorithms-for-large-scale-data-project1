# Αλγόριθμοι για Δεδομένα Ευρείας Κλίμακας — Project 1

Πρώτη εργασία στο μάθημα Αλγόριθμοι για Δεδομένα Ευρείας Κλίμακας (Τμήμα Μηχανικών Η/Υ & Πληροφορικής, Παν. Ιωαννίνων).

Ο κώδικας υλοποιεί διάφορους streaming αλγορίθμους και τρέχει πειράματα που βγάζουν διαγράμματα στον φάκελο `plots/`.

## Αρχεία (`solutions_4940/`)

- `A1_morris_counter.py` — Morris counter
- `A2_morris_exact.py` — ακριβής υπολογισμός της κατανομής του Morris counter
- `B1_distinct_counting.py` — μέτρηση μοναδικών στοιχείων (trailing zeros, Trie)
- `B2_hash_family.py` — hash family
- `B3_bjkst.py` — αλγόριθμος BJKST
- `C1_bloom_intersection.py` — Bloom filters και τομή συνόλων
- `D_packet_tracing.py` — packet tracing με Bloom filters
- `run_all.py` — τρέχει όλα τα παραπάνω
- `graph*.txt` — δεδομένα εισόδου
- `plots/` — τα διαγράμματα που παράγονται

## Εκτέλεση

Χρειάζεται Python 3 και matplotlib:

```bash
pip install matplotlib
cd solutions_4940
python run_all.py
```

Για να τρέξεις μόνο μία άσκηση, π.χ.:

```bash
python B3_bjkst.py
```

Όλα τα scripts έχουν `random.seed(42)`, οπότε βγάζουν τα ίδια αποτελέσματα κάθε φορά.

## Άλλα αρχεία

- `report_final.pdf` — η αναφορά της εργασίας
- `Φυλλάδιο Ασκήσεων 1.pdf` — η εκφώνηση

## Συγγραφέας

Αθανάσιος Φουρκιώτης
