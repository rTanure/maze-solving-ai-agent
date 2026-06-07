import math
import random
from src.utils.resultados.resultado_simulated_annealing import ResultadoSimulatedAnnealing# Você criaria essa classe baseada na sua de Hill Climbing
from src.utils.buscas.local.hill_climbing import calcular_custo_rota, gerar_vizinhos_por_troca

def simulated_annealing(maze_obj, temp_inicial = 1000, taxa_resfriamento = 0.2):
    resultado = ResultadoSimulatedAnnealing(maze_obj.id)
    resultado.start()

    
    from src.utils.menor_caminho import obter_grafo
    matriz_distancias, matriz_caminhos, pontos = obter_grafo(maze_obj)
    lista_coletaveis = [k for k in pontos.keys() if isinstance(k, tuple)]

    # 2. Estado Inicial
    estado_atual = lista_coletaveis[:]
    random.shuffle(estado_atual)
    custo_atual = calcular_custo_rota(estado_atual, matriz_distancias)
    
    melhor_estado = estado_atual[:]
    melhor_custo = custo_atual
    
    temp = temp_inicial

    iteracoes = 0
    curva_convergencia = [(0, custo_atual)]
    
    # 3. Loop de Busca
    while temp > 0.1:
        iteracoes += 1
        # Pega um vizinho usando a sua função que já funciona (troca de posições)
        vizinhos = gerar_vizinhos_por_troca(estado_atual)
        if not vizinhos:
            break
        candidato = random.choice(vizinhos)
        custo_candidato = calcular_custo_rota(candidato, matriz_distancias)
        
        # O "Pulo do Gato": Critério de aceitação probabilístico
        delta = custo_candidato - custo_atual
        if delta < 0 or random.random() < math.exp(-delta / temp):
            estado_atual = candidato
            custo_atual = custo_candidato
            
            if custo_atual < melhor_custo:
                melhor_estado = estado_atual[:]
                melhor_custo = custo_atual
                curva_convergencia.append((iteracoes, melhor_custo))
        
        temp *= taxa_resfriamento
        
    resultado.finish()
    resultado.sucesso = True
    resultado.custo = melhor_custo
    resultado.passos = iteracoes
    resultado.iteracoes = iteracoes
    resultado.curva = curva_convergencia
    
    # Salva a ordem exata dos coletáveis encontrados. Ex: [(1, 3), (5, 2)]
    resultado.ordem_coletaveis = estado_atual 
    
    # A rota macro inclui o Início e o Fim. Ex: ['A', (1, 3), (5, 2), 'B']
    rota_macro = ['A'] + melhor_estado + ['B']
    resultado.rota_macro = rota_macro

    if matriz_caminhos:
        caminho_completo = []
        for i in range(len(rota_macro) - 1):
            origem = rota_macro[i]
            destino = rota_macro[i+1]
            
            # Pega a lista de coordenadas contínuas daquele trecho específico
            trecho = matriz_caminhos[origem][destino]
            
            # Removemos a primeira coordenada dos trechos seguintes para não duplicar
            # (já que o final de um trecho é exatamente o início do próximo)
            if i > 0 and len(trecho) > 0:
                trecho = trecho[1:]
                
            caminho_completo.extend(trecho)
            
        # O .caminho final agora é uma lista gigante de (y, x) pronta para ser desenhada!
        resultado.caminho = caminho_completo
    else:
        # Fallback de segurança se esquecer de mandar a matriz_caminhos
        resultado.caminho = rota_macro
        
    return resultado