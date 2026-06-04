import heapq
from src.utils.auxiliar_busca import get_vizinhos
from src.utils.resultados.resultado_ucs import ResultadoUCS

def ucs(grid, inicio, objetivo):
    resultado = ResultadoUCS()
    resultado.start()

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
            resultado.finish()
            return caminho, resultado
            
        if atual not in visitados:
            visitados.add(atual)
            
            for vizinho in get_vizinhos(grid, atual):
                if vizinho not in visitados:
                    heapq.heappush(fila_prioridade, (custo + 1, vizinho, caminho + [vizinho]))
                    resultado.addfronteira(1)
    resultado.finish()                
    return None, resultado