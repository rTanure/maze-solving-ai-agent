import heapq
from src.utils.buscas.auxiliar_busca import get_vizinhos, encontrar_inicio_fim
from src.utils.resultados.resultado_ucs import ResultadoUCS

def ucs(maze_obj):
    resultado = ResultadoUCS(maze_obj.id)
    resultado.start()

    # Extraindo dados do objeto Maze
    grid = maze_obj.maze

    inicio, objetivo = encontrar_inicio_fim(maze_obj)

    fila_prioridade = [(0, inicio, [inicio])]
    visitados = set()
    resultado.addfronteira(1)
    
    while fila_prioridade:
        custo, atual, caminho = heapq.heappop(fila_prioridade)
        resultado.addExpandidos(1)
        
        if atual == objetivo:
            resultado.sucesso = True
            resultado.passos = len(caminho)
            resultado.custo = custo
            resultado.caminho = caminho # Salvando no objeto
            resultado.finish()
            
            return resultado # Retornando apenas o objeto
            
        if atual not in visitados:
            visitados.add(atual)
            
            for vizinho in get_vizinhos(grid, atual):
                if vizinho not in visitados:
                    heapq.heappush(fila_prioridade, (custo + 1, vizinho, caminho + [vizinho]))
                    resultado.addfronteira(1)
                    
    resultado.finish()                
    return resultado