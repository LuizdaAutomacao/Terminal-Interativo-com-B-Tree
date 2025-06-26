# Relatório – Avaliação Experimental (Versão Completa)

Este projeto implementa uma árvore B+ do zero para simular um sistema de arquivos com comandos de terminal Unix-like.

## 📊 Avaliação Experimental

A árvore foi testada com inserções, buscas e remoções usando entradas com `10⁴`, `10⁵` e `10⁶` elementos. Os testes foram automatizados via o script `benchmark_bplustree_full.py`.

Todas as operações foram executadas sobre **100% dos elementos inseridos**, o que representa um cenário mais realista e completo de uso da estrutura de dados.

O gráfico gerado (`Grafico.png`) representa o tempo total de execução de cada operação:

- Inserção de todos os elementos
- Busca de todos os elementos
- Remoção de todos os elementos

## 🧠 Complexidade Esperada

A árvore B+ possui desempenho teórico:

- Inserção: O(log n)
- Busca: O(log n)
- Remoção: O(log n)

Como a quantidade de operações cresceu linearmente com o número de elementos, o gráfico resultante também cresce suavemente. O tempo por operação continua se mantendo dentro da faixa logarítmica esperada, validando a eficiência da implementação.

## ✅ Conformidade com o Projeto

- A árvore suporta múltiplas instâncias para diretórios.
- Nós folha são duplamente encadeados.
- Todas as operações foram testadas com volume total.
- O código está modularizado e pronto para execução.

