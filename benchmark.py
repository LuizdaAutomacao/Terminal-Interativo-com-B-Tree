import time
import matplotlib.pyplot as plt
import random
import string
from arvore import BplusTree  # Certifique-se de que arvore.py esteja no mesmo diretório

# Gera nomes aleatórios para arquivos
def random_string(length=8):
    return ''.join(random.choices(string.ascii_lowercase, k=length))

# Função principal de benchmark
def benchmark_bplustree(order=4, sizes=[10_000, 100_000, 1_000_000]):
    tempos = {"insercao": [], "busca": [], "remocao": []}

    for n in sizes:
        print(f"Testando com n = {n}")
        chaves = [random_string() for _ in range(n)]
        amostra_busca = random.sample(chaves, min(1000, n))
        amostra_remocao = random.sample(chaves, min(1000, n))

        arvore = BplusTree(order)

        # Insercao
        t0 = time.time()
        for chave in chaves:
            arvore.insert(chave, chave)
        t1 = time.time()
        tempos["insercao"].append(t1 - t0)

        # Busca
        t0 = time.time()
        for chave in amostra_busca:
            arvore.search(chave)
        t1 = time.time()
        tempos["busca"].append(t1 - t0)

        # Remocao
        t0 = time.time()
        for chave in amostra_remocao:
            arvore.delete(chave)
        t1 = time.time()
        tempos["remocao"].append(t1 - t0)

    return tempos

# Plota os resultados em um gráfico
def plot_resultados(sizes, tempos):
    plt.plot(sizes, tempos["insercao"], marker='o', label="Inserção")
    plt.plot(sizes, tempos["busca"], marker='s', label="Busca")
    plt.plot(sizes, tempos["remocao"], marker='^', label="Remoção")
    plt.xlabel("Quantidade de elementos (n)")
    plt.ylabel("Tempo (segundos)")
    plt.title("Desempenho da Árvore B+")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("benchmark_bplustree.png")
    plt.show()

if __name__ == "__main__":
    tamanhos = [10_000, 100_000, 1_000_000]
    resultados = benchmark_bplustree(order=4, sizes=tamanhos)
    plot_resultados(tamanhos, resultados)
