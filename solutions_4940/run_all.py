import subprocess
import sys
import os

scripts = [
    "A1_morris_counter.py",
    "A2_morris_exact.py",
    "B1_distinct_counting.py",
    "B2_hash_family.py",
    "B3_bjkst.py",
    "C1_bloom_intersection.py",
    "D_packet_tracing.py",
]

os.chdir(os.path.dirname(os.path.abspath(__file__)))

for script in scripts:
    print("\n" + "=" * 50)
    print(f"Running: {script}")
    print("=" * 50)

    result = subprocess.run([sys.executable, script])

    if result.returncode != 0:
        print(f"ERROR in {script}")
        break