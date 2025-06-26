# 📊 Análise Empírica de Desempenho - Árvore B+

## Objetivo

O objetivo desta análise é avaliar empiricamente o desempenho da implementação da Árvore B+ com operações de:

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

## Metodologia

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

## Resultados

### Gráfico de desempenho

![Benchmark da Árvore B+](Grafico.png)

obs: A busca e remoção mostram 100% pois para se notar diferença graficamente as operações foram feitas em todos os elementos.
### Tempos medidos:

| Tamanho n | Inserção (s) | Busca (s) | Remoção (s) | log₁₀(n) |
|-----------|--------------|-----------|-------------|----------|
| 10.000    | 0.10         | 0.07      | 0.08        | 4        |
| 100.000   | 1.20         | 0.85      | 1.00        | 5        |
| 1.000.000 | 13.00        | 6.20      | 7.80        | 6        |

---

## Análise Comparativa

A análise visual e numérica mostra que:

- O crescimento dos tempos **segue uma tendência logarítmica**, conforme esperado teoricamente.
- A **inserção** é a operação mais custosa, pois envolve splits e propagação de chaves.
- A **busca** é eficiente e mais barata que as demais, mesmo com 1 milhão de elementos.
- A **remoção** é intermediária, impactada por possíveis fusões e rebalanceamentos.

A proporcionalidade com `log(n)` mostra que a estrutura mantém um excelente desempenho, mesmo para volumes elevados de dados.

---

## Conclusão

A implementação da Árvore B+ apresentou desempenho coerente com o esperado:

- Todas as operações escalaram com **crescimento logarítmico**.
- A estrutura manteve **eficiência e estabilidade** mesmo com grandes volumes de dados.
- A estratégia de **encadeamento duplo nos nós folha** contribuiu para um acesso eficiente e ordenado dos dados.
- O sistema está pronto para uso em aplicações que exijam armazenamento hierárquico com alto desempenho.

