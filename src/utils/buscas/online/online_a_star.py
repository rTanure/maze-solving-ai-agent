import heapq
from src.utils.buscas.auxiliar_busca import get_vizinhos, heuristica_manhattan, encontrar_inicio_fim
from src.utils.resultados.resultado_online_a_star import ResultadoOnlineAStar

def _a_star_replanejamento(grid_interno, inicio, objetivo, resultado_tracker):
    h_inicio = heuristica_manhattan(inicio, objetivo)
    
    # OTIMIZAÇÃO 1: Retiramos a lista 'caminho' de dentro da tupla. 
    # A tupla agora é muito mais leve: (f_cost, g_cost, atual)
    fila_prioridade = [(h_inicio, 0, inicio)]
    
    # Dicionários para controle de custo e para reconstruir o caminho sem estourar a RAM
    g_costs = {inicio: 0}
    came_from = {inicio: None}
    
    resultado_tracker.addfronteira(1)
    
    while fila_prioridade:
        if len(fila_prioridade) > resultado_tracker.fronteira:
            resultado_tracker.fronteira = len(fila_prioridade)
            
        _, g_cost, atual = heapq.heappop(fila_prioridade)
        resultado_tracker.addExpandidos(1)
        
        if atual == objetivo:
            # Reconstrói o caminho de trás pra frente através dos ponteiros
            caminho = []
            passo = atual
            while passo is not None:
                caminho.append(passo)
                passo = came_from[passo]
            return caminho[::-1] # Inverte a lista para ficar do Início -> Fim
            
        # Pula processamento de nós obsoletos se já achamos uma rota mais barata pra eles
        if g_cost > g_costs.get(atual, float('inf')):
            continue
            
        for vizinho in get_vizinhos(grid_interno, atual):
            novo_g = g_cost + 1
            
            # Só adiciona na fila se for um caminho melhor para aquele vizinho
            if novo_g < g_costs.get(vizinho, float('inf')):
                g_costs[vizinho] = novo_g
                novo_f = novo_g + heuristica_manhattan(vizinho, objetivo)
                
                heapq.heappush(fila_prioridade, (novo_f, novo_g, vizinho))
                came_from[vizinho] = atual # Vizinho 'lembra' quem é o pai dele
                resultado_tracker.addfronteira(1)
                    
    return None

def online_a_star(maze_obj, dados_adicionais=None):
    resultado = ResultadoOnlineAStar(maze_obj.id)
    resultado.start()
    
    grid_real = maze_obj.maze
    
    if dados_adicionais and 'inicio_override' in dados_adicionais:
        inicio = dados_adicionais['inicio_override']
        objetivo = dados_adicionais['objetivo_override']
    else:
        inicio, objetivo = encontrar_inicio_fim(maze_obj)
        
    if not inicio or not objetivo:
        resultado.sucesso = False
        resultado.finish()
        return resultado
        
    altura = len(grid_real)
    largura = len(grid_real[0])
    
    grid_interno = [['?' for _ in range(largura)] for _ in range(altura)]
    grid_interno[inicio[1]][inicio[0]] = 'A'
    grid_interno[objetivo[1]][objetivo[0]] = 'B'
    
    atual = inicio
    caminho_percorrido = [atual]
    
    celulas_conhecidas = {atual}
    visitados_fisicamente = {atual}
    
    while atual != objetivo:
        x, y = atual
        direcoes = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        
        # FASE 1: Perceber
        for dx, dy in direcoes:
            nx, ny = x + dx, y + dy
            if 0 <= ny < altura and 0 <= nx < largura:
                if (nx, ny) not in celulas_conhecidas:
                    estado_real = grid_real[ny][nx]
                    grid_interno[ny][nx] = estado_real
                    celulas_conhecidas.add((nx, ny))
                    resultado.celulas_reveladas += 1

        # FASE 2: Planejar
        resultado.replanejamentos += 1
        caminho_planejado = _a_star_replanejamento(grid_interno, atual, objetivo, resultado)
        
        if not caminho_planejado or len(caminho_planejado) < 2:
            resultado.caminho = caminho_percorrido
            resultado.finish()
            return resultado 
                
        # FASE 3: Agir
        proximo_passo = caminho_planejado[1]
        proximo_x, proximo_y = proximo_passo

        if grid_real[proximo_y][proximo_x] == '#':
            grid_interno[proximo_y][proximo_x] = '#'
            celulas_conhecidas.add(proximo_passo)
            resultado.celulas_reveladas += 1
            continue
        
        if proximo_passo in visitados_fisicamente:
            resultado.celulas_revisitadas += 1
            
        visitados_fisicamente.add(proximo_passo)
        atual = proximo_passo
        caminho_percorrido.append(atual)
        
        resultado.addPassos(1)
        resultado.addCusto(1)
        
    resultado.sucesso = True
    resultado.caminho = caminho_percorrido
    resultado.finish()
    
    return resultado
# import heapq
# from src.utils.buscas.auxiliar_busca import get_vizinhos, heuristica_manhattan, encontrar_inicio_fim
# from src.utils.resultados.resultado_online_a_star import ResultadoOnlineAStar

# def _a_star_replanejamento(grid_interno, inicio, objetivo, resultado_tracker):
#     h_inicio = heuristica_manhattan(inicio, objetivo)
#     fila_prioridade = [(h_inicio, 0, inicio, [inicio])]
#     visitados = set()
    
#     resultado_tracker.addfronteira(1)
    
#     while fila_prioridade:
#         # Atualiza métrica de fronteira máxima interna
#         if len(fila_prioridade) > resultado_tracker.fronteira:
#             resultado_tracker.fronteira = len(fila_prioridade)
            
#         _, g_cost, atual, caminho = heapq.heappop(fila_prioridade)
#         resultado_tracker.addExpandidos(1)
        
#         if atual == objetivo:
#             return caminho
            
#         if atual not in visitados:
#             visitados.add(atual)
            
#             for vizinho in get_vizinhos(grid_interno, atual):
#                 if vizinho not in visitados:
#                     novo_g = g_cost + 1
#                     novo_f = novo_g + heuristica_manhattan(vizinho, objetivo)
#                     heapq.heappush(fila_prioridade, (novo_f, novo_g, vizinho, caminho + [vizinho]))
                    
#     return None

# def online_a_star(maze_obj, dados_adicionais=None):
#     resultado = ResultadoOnlineAStar(maze_obj.id)
#     resultado.start()
    
#     # Extraindo dados do objeto Maze
#     grid_real = maze_obj.maze
    
#     if dados_adicionais and 'inicio_override' in dados_adicionais:
#         inicio = dados_adicionais['inicio_override']
#         objetivo = dados_adicionais['objetivo_override']
#     else:
#         inicio, objetivo = encontrar_inicio_fim(maze_obj)
        
#     # Validação de segurança
#     if not inicio or not objetivo:
#         resultado.sucesso = False
#         resultado.finish()
#         return resultado
        
#     altura = len(grid_real)
#     largura = len(grid_real[0])
    
#     # Inicializa o mapa interno
#     grid_interno = [['?' for _ in range(largura)] for _ in range(altura)]
#     grid_interno[inicio[0]][inicio[1]] = 'A'
#     grid_interno[objetivo[0]][objetivo[1]] = 'B'
    
#     atual = inicio
#     caminho_percorrido = [atual]
    
#     celulas_conhecidas = {atual}
#     visitados_fisicamente = {atual}
    
#     while atual != objetivo:
#         y, x = atual
#         direcoes = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        
#         # FASE 1: Perceber
#         for dy, dx in direcoes:
#             ny, nx = y + dy, x + dx
#             if 0 <= ny < altura and 0 <= nx < largura:
#                 if (ny, nx) not in celulas_conhecidas:
#                     grid_interno[ny][nx] = grid_real[ny][nx]
#                     celulas_conhecidas.add((ny, nx))
#                     resultado.celulas_reveladas += 1

#         # FASE 2: Planejar
#         resultado.replanejamentos += 1
#         caminho_planejado = _a_star_replanejamento(grid_interno, atual, objetivo, resultado)
        
#         # Sem saída baseada no mapa atual
#         if not caminho_planejado or len(caminho_planejado) < 2:
#             resultado.caminho = caminho_percorrido
#             resultado.finish()
#             return resultado 
            
#         # FASE 3: Agir
#         proximo_passo = caminho_planejado[1]
        
#         if proximo_passo in visitados_fisicamente:
#             resultado.celulas_revisitadas += 1
            
#         visitados_fisicamente.add(proximo_passo)
#         atual = proximo_passo
#         caminho_percorrido.append(atual)
        
#         resultado.addPassos(1)
#         resultado.addCusto(1)
        
#     # Sucesso
#     resultado.sucesso = True
#     resultado.caminho = caminho_percorrido
#     resultado.finish()
    
#     return resultado
