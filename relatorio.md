# 📊 Análise Empírica e Estrutural do Sistema Fakerational com Árvore B+

---

## 1. Objetivo

O objetivo desta análise é avaliar o desempenho e o funcionamento estrutural da **Árvore B+** usada no sistema de arquivos `fakerational`.

Serão abordados:

- A complexidade teórica e empírica das operações (inserção, busca e remoção);
- A estrutura hierárquica formada por árvores B+ nos diretórios;
- O funcionamento do terminal e os comandos que impactam essa estrutura.

---

## 2. Metodologia Experimental

O script `benchmark.py` foi utilizado para medir os tempos totais (em segundos) de três operações:

- Inserção de `n` elementos aleatórios;
- Busca por todos os elementos inseridos;
- Remoção completa dos elementos.

Os testes foram realizados para:

- **n = 10.000**
- **n = 100.000**
- **n = 1.000.000**

Os dados foram visualizados no gráfico `Grafico.png`.

---

## 3. Estrutura Hierárquica das Árvores B+

### 3.1 Conceito

O sistema fakerational organiza seus dados como **uma hierarquia de árvores B+ aninhadas**:

- Cada diretório possui sua própria instância de B+ Tree.
- Arquivos são armazenados nas folhas.
- Os nós internos representam diretórios, contendo ponteiros para subárvores.

### 3.2 Exemplo Visual

Abaixo, um exemplo visual da estrutura gerada:

![Estrutura de Árvores B+](Esquema_visual.png)

### 3.3 Comandos utilizados para gerar a estrutura:

```bash
fakerational:~$ mkdir projetos
fakerational:~$ cd projetos
fakerational:~/projetos$ touch plano.txt
fakerational:~/projetos$ mkdir relatorios
fakerational:~/projetos$ mkdir testes
fakerational:~/projetos/relatorios$ touch abril.pdf
fakerational:~/projetos/relatorios$ touch maio.pdf
fakerational:~/projetos/testes$ touch unit.py
fakerational:~/projetos/testes$ touch integracao.py
