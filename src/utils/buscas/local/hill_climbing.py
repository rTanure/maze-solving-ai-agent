import random
import time

def calcular_custo_rota(ordem_coleta, matriz_distancias):
    if not ordem_coleta:
        return matriz_distancias['A']['B']

    custo_total = matriz_distancias['A'][ordem_coleta[0]]

    for i in range(len(ordem_coleta) - 1):
        origem = ordem_coleta[i]
        destino = ordem_coleta[i+1]
        custo_total += matriz_distancias[origem][destino]

    custo_total += matriz_distancias[ordem_coleta[-1]]['B']

    return custo_total

def gerar_vizinhos_por_troca(ordem_atual):

    vizinhos = []
    n = len(ordem_atual)
   
    for i in range(n):
        for j in range(i + 1, n):
            vizinho = ordem_atual[:] 
            vizinho[i], vizinho[j] = vizinho[j], vizinho[i]
            vizinhos.append(vizinho)
            
    return vizinhos

def executar_hill_climbing_tsp(matriz_distancias, lista_coletaveis):
    estado_atual = lista_coletaveis[:]
    random.shuffle(estado_atual) 
    custo_atual = calcular_custo_rota(estado_atual, matriz_distancias)
    
    iteracoes = 0
    curva_convergencia = [(iteracoes, custo_atual)]
    
    inicio_tempo = time.perf_counter()

    while True:
        iteracoes += 1
        vizinhos = gerar_vizinhos_por_troca(estado_atual)
        
        melhor_vizinho = None
        melhor_custo_vizinho = float('inf')

        for vizinho in vizinhos:
            custo_vizinho = calcular_custo_rota(vizinho, matriz_distancias)
            
            if custo_vizinho < melhor_custo_vizinho:
                melhor_custo_vizinho = custo_vizinho
                melhor_vizinho = vizinho
                

        if melhor_custo_vizinho < custo_atual:
            estado_atual = melhor_vizinho
            custo_atual = melhor_custo_vizinho
            curva_convergencia.append((iteracoes, custo_atual))
        else:

            break

    fim_tempo = time.perf_counter()

    rota_final = ['A'] + estado_atual + ['B'] 

    return {
        'rota': rota_final,
        'custo': custo_atual,
        'iteracoes': iteracoes,
        'tempo_s': fim_tempo - inicio_tempo,
        'curva': curva_convergencia
    }