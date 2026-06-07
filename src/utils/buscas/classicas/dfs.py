from src.utils.buscas.auxiliar_busca import get_vizinhos, encontrar_inicio_fim
from src.utils.resultados.resultado_dfs import ResultadoDFS

def dfs(maze_obj):
    resultado = ResultadoDFS()
    resultado.start()

    # Extraindo dados do objeto Maze
    grid = maze_obj.maze
    inicio, objetivo = encontrar_inicio_fim(grid)

    pilha = [(inicio, [inicio])]
    visitados = set()
    resultado.addfronteira(1)
    
    while pilha:
        atual, caminho = pilha.pop()
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
                    pilha.append((vizinho, caminho + [vizinho]))
                    resultado.addfronteira(1)
                    
    resultado.finish()                
    return resultado