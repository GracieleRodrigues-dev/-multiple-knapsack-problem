# -multiple-knapsack-problem

# Problema de Múltiplas Mochilas (Knapsack Problem) com Pyomo

Este projeto implementa uma solução para o problema de múltiplas (Multiple Knapsack Problem) utilizando a biblioteca Pyomo. O algoritmo lê instâncias do problema a partir de arquivos de entrada, resolve o problema de otimização e salva os resultados em arquivos de saída.

## Estrutura dos Arquivos

O projeto contém os seguintes diretórios e arquivos:

- `./instances/`: Diretório que contém os arquivos de entrada. Cada arquivo deve seguir a seguinte estrutura:
    - A primeira linha deve conter dois números inteiros: `n` (número de itens) e `m` (número de mochilas).
    - As próximas `n` linhas devem conter dois números flutuantes: o valor e o peso de cada item.
    - A última linha deve conter `m` números flutuantes, representando as capacidades das mochilas.
  
- `./outputs/`: Diretório onde os resultados serão salvos. Os arquivos de saída contêm o tempo de execução e a solução ótima para cada instância lida. Toda vez que o algoritmo é executado os arquivos são sobrescritos.

- `knapsack.py`: O script principal que contém a implementação do algoritmo.

## Requisitos

Para executar este projeto, você precisa ter o Python instalado juntamente com as seguintes bibliotecas:

- Pyomo
- GLPK

Você pode instalar as dependências necessárias usando o pip:

```bash
pip install pyomo
```

Para executar o código, execute o seguinte comando no terminal:

```bash
python multiple-knapsack.py
```