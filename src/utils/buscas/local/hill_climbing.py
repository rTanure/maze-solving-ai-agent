import random
from src.utils.resultados.resultado_hill_climbing import ResultadoHillClimbing

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

def hill_climbing(maze_obj):
    # 1. INICIALIZA O RESULTADO AQUI (faltava no seu snippet!)
    resultado = ResultadoHillClimbing(maze_obj.id)
    resultado.start()

    from src.utils.menor_caminho import obter_grafo
    matriz_distancias, matriz_caminhos, pontos = obter_grafo(maze_obj)

    print("PONTOS:", pontos)
    print("COLETAVEIS:", lista_coletaveis)

    lista_coletaveis = [k for k in pontos.keys() if isinstance(k, tuple)]
    # ---------------------------------------------------

    estado_atual = lista_coletaveis[:]
    random.shuffle(estado_atual)
    custo_atual = calcular_custo_rota(estado_atual, matriz_distancias)
    
    iteracoes = 0
    curva_convergencia = [(iteracoes, custo_atual)]

    while True:
        iteracoes += 1
        resultado.addExpandidos(1) 
        
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

    resultado.finish()

    # --- PREENCHENDO OS DADOS ESTATÍSTICOS ---
    resultado.sucesso = True
    resultado.custo = custo_atual
    resultado.passos = iteracoes
    resultado.iteracoes = iteracoes
    resultado.curva = curva_convergencia
    
    # Salva a ordem exata dos coletáveis encontrados. Ex: [(1, 3), (5, 2)]
    resultado.ordem_coletaveis = estado_atual 
    
    # A rota macro inclui o Início e o Fim. Ex: ['A', (1, 3), (5, 2), 'B']
    rota_macro = ['A'] + estado_atual + ['B']
    resultado.rota_macro = rota_macro

    # --- COSTURANDO O CAMINHO COMPLETO DE COORDENADAS ---
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