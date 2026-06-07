import heapq
from src.utils.buscas.auxiliar_busca import get_vizinhos, heuristica_manhattan, encontrar_inicio_fim
from src.utils.resultados.resultado_a_star import ResultadoAStar

def a_star(maze_obj):
    resultado = ResultadoAStar(maze_obj.id)
    resultado.start()
    
    # Extraindo dados do objeto Maze
    grid = maze_obj.maze
    inicio, objetivo = encontrar_inicio_fim(maze_obj)
    
    h_inicio = heuristica_manhattan(inicio, objetivo)
    
    fila_prioridade = [(h_inicio, 0, inicio, [inicio])]
    visitados = set()
    
    resultado.addfronteira(1)
    
    while fila_prioridade:
        if len(fila_prioridade) > resultado.fronteira:
            resultado.fronteira = len(fila_prioridade)
            
        f_cost, g_cost, atual, caminho = heapq.heappop(fila_prioridade)
        
        resultado.addExpandidos(1)
        
        if atual == objetivo:
            resultado.sucesso = True
            resultado.passos = len(caminho)
            resultado.custo = g_cost
            resultado.caminho = caminho # Salvando no objeto
            resultado.finish()
            
            return resultado # Retornando apenas o objeto
            
        if atual not in visitados:
            visitados.add(atual)
            
            for vizinho in get_vizinhos(grid, atual):
                if vizinho not in visitados:
                    novo_g = g_cost + 1
                    novo_f = novo_g + heuristica_manhattan(vizinho, objetivo)
                    
                    heapq.heappush(fila_prioridade, (novo_f, novo_g, vizinho, caminho + [vizinho]))
                    resultado.addfronteira(1)
                    
    resultado.finish()
    return resultado