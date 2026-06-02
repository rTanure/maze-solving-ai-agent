from collections import deque
from utils.auxiliar_busca import get_vizinhos
from utils.resultados.resultado_bfs import ResultadoBFS

def bfs(grid, inicio, objetivo):
    resultado = ResultadoBFS()
    resultado.start()
    
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
            resultado.finish()
            
            return caminho, resultado
            
        for vizinho in get_vizinhos(grid, atual):
            if vizinho not in visitados:
                visitados.add(vizinho)
                fila.append((vizinho, caminho + [vizinho]))
                resultado.addfronteira(1) 
                
    resultado.finish()
    return None, resultado