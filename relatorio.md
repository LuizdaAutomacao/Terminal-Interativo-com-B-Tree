# 📊 Análise Empírica de Desempenho - Árvore B+

---

## 🎯 Objetivo

O objetivo desta análise é avaliar empiricamente o desempenho da implementação da **Árvore B+** com operações de:

- Inserção
- Busca
- Remoção

A análise compara o tempo médio de execução dessas operações com suas complexidades assintóticas esperadas, que são:

| Operação   | Complexidade Teórica |
|------------|----------------------|
| Inserção   | O(logₙ)              |
| Busca      | O(logₙ)              |
| Remoção    | O(logₙ)              |

---

## 🧪 Metodologia

O script `benchmark.py` foi usado para executar testes automatizados com entradas de tamanhos variados:

- **n = 10.000**
- **n = 100.000**
- **n = 1.000.000**

Para cada tamanho `n`, foram medidos os tempos totais (em segundos) para:

1. Inserir `n` chaves aleatórias (strings).
2. Buscar as `n` chaves inseridas.
3. Remover as `n` chaves.

Os dados foram plotados em um gráfico (`Grafico.png`) usando `matplotlib`.

---

## 🌲 Estrutura Hierárquica das Árvores B+

### 🗂️ Representação Visual

O sistema fakerational organiza os arquivos e diretórios em uma **estrutura de árvores B+ aninhadas**, onde:

- Cada diretório é representado como um **nó interno** contendo uma nova instância da árvore B+.
- Arquivos são elementos terminais (folhas).
- A ordenação é **lexicográfica** e mantida automaticamente pela árvore.

Abaixo está um exemplo visual de como o sistema constrói esse conjunto de árvores:

![Estrutura de Árvores B+](Esquema_visual.png)

### 💻 Comandos que geram essa estrutura

Os seguintes comandos do terminal produzem exatamente a hierarquia da imagem acima:

```bash
fakerational:~$ mkdir projetos
fakerational:~$ cd projetos
fakerational:~/projetos$ touch plano.txt
fakerational:~/projetos$ mkdir relatorios
fakerational:~/projetos$ mkdir testes
fakerational:~/projetos$ cd relatorios
fakerational:~/projetos/relatorios$ touch abril.pdf
fakerational:~/projetos/relatorios$ touch maio.pdf
fakerational:~/projetos/relatorios$ cd ..
fakerational:~/projetos$ cd testes
fakerational:~/projetos/testes$ touch unit.py
fakerational:~/projetos/testes$ touch integracao.py


