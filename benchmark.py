import time
import random
import string
import matplotlib.pyplot as plt
from arvore import BplusTree

def random_string(length=8):
    return ''.join(random.choices(string.ascii_lowercase, k=length))

def benchmark_total_operacoes(tree_order, sizes):
    results = {
        "insertion": [],
        "search": [],
        "deletion": []
    }

    for n in sizes:
        keys = [random_string() for _ in range(n)]
        tree = BplusTree(tree_order)

        start = time.time()
        for key in keys:
            tree.insert(key, key)
        results["insertion"].append(time.time() - start)

        start = time.time()
        for key in keys:
            tree.search(key)
        results["search"].append(time.time() - start)

        start = time.time()
        for key in keys:
            tree.delete(key)
        results["deletion"].append(time.time() - start)

    return results

if __name__ == "__main__":
    tree_order = 4
    sizes = [10_000, 100_000, 1_000_000]

    results = benchmark_total_operacoes(tree_order, sizes)

    plt.figure()
    plt.plot(sizes, results["insertion"], marker='o', label="Inserção")
    plt.plot(sizes, results["search"], marker='s', label="Busca (100%)")
    plt.plot(sizes, results["deletion"], marker='^', label="Remoção (100%)")
    plt.xlabel("Número de elementos (n)")
    plt.ylabel("Tempo total (s)")
    plt.title("Benchmark da Árvore B+ com Operações Completas")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("benchmark_bplustree_full.png")
    plt.show()
