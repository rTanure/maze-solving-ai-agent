import heapq
from src.utils.buscas.auxiliar_busca import get_vizinhos, heuristica_manhattan, encontrar_inicio_fim
from src.utils.resultados.resultado_guloso import ResultadoGuloso

def busca_gulosa(maze_obj):
    resultado = ResultadoGuloso()
    resultado.start()
   
    # Extraindo dados do objeto Maze
    grid = maze_obj.maze
    inicio, objetivo = encontrar_inicio_fim(grid)
   
    fila_prioridade = [(heuristica_manhattan(inicio, objetivo), inicio, [inicio])]
    visitados = set()

    resultado.addfronteira(1)
    
    while fila_prioridade:
        _, atual, caminho = heapq.heappop(fila_prioridade)

        resultado.addExpandidos(1)
        
        if atual == objetivo:
            resultado.sucesso = True
            resultado.passos = len(caminho)
            resultado.custo = len(caminho) - 1
            resultado.caminho = caminho # Salvando no objeto
            resultado.finish()

            return resultado # Retornando apenas o objeto
            
        if atual not in visitados:
            visitados.add(atual)
            
            for vizinho in get_vizinhos(grid, atual):
                if vizinho not in visitados:
                    h = heuristica_manhattan(vizinho, objetivo)
                    heapq.heappush(fila_prioridade, (h, vizinho, caminho + [vizinho]))

                    resultado.addfronteira(1)
                    
    resultado.finish()               
    return resultado