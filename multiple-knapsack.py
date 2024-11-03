from pyomo.environ import *
from glob import glob
import time
import os

n = None  # Número de itens
m = None  # Número de mochilas
capacities = None  # Capacidades das mochilas
values = None  # Valores dos itens
weights = None  # Pesos dos itens

def read_instance(instance):
    global n, m, capacities, values, weights
    values = []
    weights = []
    capacities = []
    
    with open(instance, 'r') as file:
        lines = file.readlines()
        first = True
        for i, line in enumerate(lines):
            if first:
                n, m = map(int, line.split())
                first = False
                continue
            data = list(map(float, line.split()))
            if len(data) == 2:  # Linhas de itens
                values.append(data[0])
                weights.append(data[1])
            # Captura as capacidades de cada mochila na última linha
            if i == len(lines) - 1:  # Se for a última linha
                capacities = data 

    print(f"Lido da instância: n={n}, m={m}, values={values}, weights={weights}, capacities={capacities}")

def solve(instance):
    # Extrai o nome base do arquivo de instância para o nome do output
    output_filename = f"./outputs/output_{os.path.basename(instance)}.txt"
    
    # Criação do modelo
    model = ConcreteModel()

    # Variáveis de decisão
    model.x = Var(range(m), range(n), domain=Boolean)

    # Função objetivo
    model.obj = Objective(expr=sum(model.x[i, j] * values[j] for i in range(m) for j in range(n)), sense=maximize)

    # Restrições de capacidade para cada mochila
    model.capacity_constraints = ConstraintList()
    for i in range(m):
        model.capacity_constraints.add(expr=sum(model.x[i, j] * weights[j] for j in range(n)) <= capacities[i])

    # Restrição de exclusividade para cada item
    model.item_exclusivity = ConstraintList()
    for j in range(n):
        model.item_exclusivity.add(expr=sum(model.x[i, j] for i in range(m)) <= 1)

    # Solução e medição de tempo
    start_time = time.time()
    opt = SolverFactory('glpk')
    results = opt.solve(model, tee=False)
    end_time = time.time()
    elapsed_time = end_time - start_time

    # Gravação dos resultados no arquivo de saída
    with open(output_filename, 'w',encoding='utf-8') as output_file:
        output_file.write(f"Tempo de execução: {elapsed_time:.4f} segundos\n")
        output_file.write("Solução ótima:\n")
        
        for i in range(m):
            items_in_knapsack = [j + 1 for j in range(n) if model.x[i, j]() > 0.5]  # Itens alocados à mochila
            total_weight = sum(weights[j] for j in range(n) if model.x[i, j]() > 0.5)  # Peso total na mochila
            total_value = sum(values[j] for j in range(n) if model.x[i, j]() > 0.5)  # Valor total na mochila
            original_capacity = capacities[i]  # Capacidade original da mochila
                
            output_file.write(f"Mochila {i + 1}: ")
            if items_in_knapsack:
                output_file.write(", ".join(map(str, items_in_knapsack)) + "\n")
                output_file.write(f"  Peso total: {total_weight}, Valor total: {total_value}, Capacidade original: {original_capacity}\n")
            else:
                output_file.write("nenhum item\n")
                output_file.write(f"  Peso total: 0, Valor total: 0, Capacidade original: {original_capacity}\n")
                
    print(f"Resultado salvo em {output_filename}")

# Processamento de múltiplas instâncias
for instance in glob('./instances/*'):
    read_instance(instance)
    solve(instance)
