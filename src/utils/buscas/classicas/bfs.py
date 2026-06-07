from collections import deque
from src.utils.buscas.auxiliar_busca import get_vizinhos, encontrar_inicio_fim
from src.utils.resultados.resultado_bfs import ResultadoBFS

def bfs(maze_obj):
    resultado = ResultadoBFS(maze_obj.id)
    resultado.start()
    
    # Extraindo dados do objeto Maze
    grid = maze_obj.maze
    inicio, objetivo = encontrar_inicio_fim(grid)
    
    fila = deque([(inicio, [inicio])])
    visitados = {inicio}
    resultado.addfronteira(1) 
    
    while fila:
        atual, caminho = fila.popleft()
        resultado.addExpandidos(1) 
        
        if atual == objetivo:
            resultado.sucesso = True
            resultado.passos = len(caminho)
            resultado.custo = len(caminho) - 1 
            resultado.caminho = caminho # Salvando no objeto
            resultado.finish()
            
            return resultado # Retornando apenas o objeto
            
        for vizinho in get_vizinhos(grid, atual):
            if vizinho not in visitados:
                visitados.add(vizinho)
                fila.append((vizinho, caminho + [vizinho]))
                resultado.addfronteira(1) 
                
    resultado.finish()
    return resultado