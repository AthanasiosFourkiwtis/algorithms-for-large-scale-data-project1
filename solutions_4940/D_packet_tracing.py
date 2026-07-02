import os
import random
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

random.seed(42)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
GRAPHS_DIR = BASE_DIR
PLOTS_DIR = os.path.join(BASE_DIR, "plots")
os.makedirs(PLOTS_DIR, exist_ok=True)

BLOOM_SIZE = 10000
NUM_MESSAGES = 100000
NUM_SOURCE_ROUTERS = 10
p = 1048583   # a prime slightly above 2^20


# ----------------helper functions----------------

def split_100bit(x):
    parts = []
    for _ in range(5):
        parts.append(x & ((1 << 20) - 1))
        x >>= 20
    return parts[::-1]


def make_hash(alpha, beta, N):
    def h(x):
        c = 0
        for part in split_100bit(x):
            c = (alpha * (part + c) + beta) % p
        return c % N
    return h


def load_graph(filename):
    with open(filename) as f:
        n, m = map(int, f.readline().split())

        adj_out = {i: [] for i in range(1, n + 1)}
        adj_in = {i: [] for i in range(1, n + 1)}

        for _ in range(m):
            x, y = map(int, f.readline().split())
            adj_out[x].append(y)
            adj_in[y].append(x)

    return n, adj_out, adj_in


# ----------------main simulation----------------

def simulate_and_trace(n, adj_out, adj_in, k_hash):
    # one Bloom filter per router
    bloom_filters = [bytearray((BLOOM_SIZE + 7) // 8) for _ in range(n + 1)]

    # each router's hash functions
    router_hashes = [[] for _ in range(n + 1)]
    for router in range(1, n + 1):
        for _ in range(k_hash):
            a = random.randint(1, p - 1)
            b = random.randint(0, p - 1)
            router_hashes[router].append(make_hash(a, b, BLOOM_SIZE))

    # insert into the Bloom filter
    def bf_add(router, msg):
        for h in router_hashes[router]:
            pos = h(msg)
            byte_index = pos >> 3
            bit_index = pos & 7
            bloom_filters[router][byte_index] |= (1 << bit_index)

    # look up in the Bloom filter
    def bf_check(router, msg):
        for h in router_hashes[router]:
            pos = h(msg)
            byte_index = pos >> 3
            bit_index = pos & 7
            if not (bloom_filters[router][byte_index] & (1 << bit_index)):
                return False
        return True

    messages = []
    true_sources = []

    for _ in range(NUM_MESSAGES):
        msg = random.randint(0, 2**100 - 1)
        source = random.randint(1, NUM_SOURCE_ROUTERS)

        messages.append(msg)
        true_sources.append(source)

        current = source
        bf_add(current, msg)

        visited_on_path = {current}

        while current != n:
            next_nodes = adj_out[current]

            if not next_nodes:
                break

            # avoid cycles as much as possible
            choices = [v for v in next_nodes if v not in visited_on_path]
            if not choices:
                choices = next_nodes

            current = random.choice(choices)
            visited_on_path.add(current)
            bf_add(current, msg)

    successful = 0

    for msg, real_source in zip(messages, true_sources):
        stack = [n]
        visited = set()
        claimed_sources = set()

        while stack:
            router = stack.pop()

            if router in visited:
                continue
            visited.add(router)

            if not bf_check(router, msg):
                continue

            # if it is a source router
            if 1 <= router <= NUM_SOURCE_ROUTERS:
                claimed_sources.add(router)
            else:
                for pred in adj_in[router]:
                    if pred not in visited:
                        stack.append(pred)

        if claimed_sources == {real_source}:
            successful += 1

    return successful


# ----------------main----------------

hash_func_options = [1, 2, 3, 5, 7, 10]

graph_files = sorted(
    f for f in os.listdir(GRAPHS_DIR)
    if f.startswith("graph") and f.endswith(".txt")
)

results_by_graph = {}

for gf in graph_files:
    graph_name = gf.replace(".txt", "")
    path = os.path.join(GRAPHS_DIR, gf)

    n, adj_out, adj_in = load_graph(path)

    print("\n" + "=" * 50)
    print("Graph:", graph_name)
    print("k_hash   successful   rate")

    results_by_graph[graph_name] = {}

    for k_hash in hash_func_options:
        random.seed(42)
        succ = simulate_and_trace(n, adj_out, adj_in, k_hash)
        rate = succ / NUM_MESSAGES

        print(k_hash, succ, rate)

        results_by_graph[graph_name][k_hash] = succ

# ----------------plot----------------

n_graphs = len(results_by_graph)
fig, axes = plt.subplots(1, n_graphs, figsize=(4 * n_graphs, 5))

if n_graphs == 1:
    axes = [axes]

for ax, (name, res) in zip(axes, results_by_graph.items()):
    ks = sorted(res.keys())
    rates = [res[k] / NUM_MESSAGES * 100 for k in ks]

    ax.plot(ks, rates, marker="o")
    ax.set_title(name)
    ax.set_xlabel("Number of hash functions")
    ax.set_ylabel("Successful trace rate (%)")
    ax.set_ylim(0, 105)
    ax.grid(True, alpha=0.4)

plt.tight_layout()
plot_path = os.path.join(PLOTS_DIR, "D_packet_tracing.png")
plt.savefig(plot_path)
plt.close()

print("\nPlot saved to", plot_path)

# ── Part Dβ ───────────────────────────────────────────────────────

print("""
The successful trace rate depends on the path length: at every router
a message crosses, the message is recorded in that router's Bloom
filter. During the reverse trace, any router that yields a
false positive spreads the search
in wrong directions. Graphs with a small average path length
expose each message to fewer routers, hence fewer false positives and
better tracing.
Topology width matters next: graphs with many branches make
tracing harder because there are many different paths
back to the sources — more routers get checked during the
reverse search, increasing false positive hits.
Finally, the number of hash functions (k) has an optimum: the theoretically best value is k = (N/n)·ln2
where N=10,000 bits and n = the average number of messages per router.
Too few hash functions means a high false positive rate.
Too many hash functions fills the filter quickly, which also drives FP up,
so the best value is found experimentally.
""")
