import heapq
from src.utils.auxiliar_busca import get_vizinhos, heuristica_manhattan
from src.utils.resultados.resultado_online_a_star import ResultadoOnlineAStar

def _a_star_replanejamento(grid_interno, inicio, objetivo, resultado_tracker):
    h_inicio = heuristica_manhattan(inicio, objetivo)
    fila_prioridade = [(h_inicio, 0, inicio, [inicio])]
    visitados = set()
    
    resultado_tracker.addfronteira(1)
    
    while fila_prioridade:
        f_cost, g_cost, atual, caminho = heapq.heappop(fila_prioridade)
        resultado_tracker.addExpandidos(1)
        
        if atual == objetivo:
            return caminho
            
        if atual not in visitados:
            visitados.add(atual)
            
            for vizinho in get_vizinhos(grid_interno, atual):
                if vizinho not in visitados:
                    novo_g = g_cost + 1
                    novo_f = novo_g + heuristica_manhattan(vizinho, objetivo)
                    heapq.heappush(fila_prioridade, (novo_f, novo_g, vizinho, caminho + [vizinho]))
                    resultado_tracker.addfronteira(1)
                    
    return None

def online_a_star(grid_real, inicio, objetivo):
    resultado = ResultadoOnlineAStar()
    resultado.start()
    
    altura = len(grid_real)
    largura = len(grid_real[0])
    
    grid_interno = [['?' for _ in range(largura)] for _ in range(altura)]
    grid_interno[inicio[0]][inicio[1]] = 'A'
    grid_interno[objetivo[0]][objetivo[1]] = 'B'
    
    atual = inicio
    caminho_percorrido = [atual]
    
    celulas_conhecidas = {atual}
    visitados_fisicamente = {atual}
    
    while atual != objetivo:
        y, x = atual
        direcoes = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        
        for dy, dx in direcoes:
            ny, nx = y + dy, x + dx
            if 0 <= ny < altura and 0 <= nx < largura:
                if (ny, nx) not in celulas_conhecidas:
                    grid_interno[ny][nx] = grid_real[ny][nx]
                    celulas_conhecidas.add((ny, nx))
                    resultado.celulas_reveladas += 1

        resultado.replanejamentos += 1
        caminho_planejado = _a_star_replanejamento(grid_interno, atual, objetivo, resultado)
        
        if not caminho_planejado or len(caminho_planejado) < 2:
            resultado.finish()
            return caminho_percorrido, resultado
            
        proximo_passo = caminho_planejado[1]
        
        if proximo_passo in visitados_fisicamente:
            resultado.celulas_revisitadas += 1
            
        visitados_fisicamente.add(proximo_passo)
        atual = proximo_passo
        caminho_percorrido.append(atual)
        
        resultado.addPassos(1)
        resultado.addCusto(1)
        
    resultado.sucesso = True
    resultado.finish()
    
    return caminho_percorrido, resultado