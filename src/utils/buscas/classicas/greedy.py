import heapq
from utils.auxiliar_busca import get_vizinhos, heuristica_manhattan
from utils.resultados.resultado_guloso import ResultadoGuloso

def busca_gulosa(grid, inicio, objetivo):
    resultado = ResultadoGuloso()
    resultado.start()
   
    fila_prioridade = [(heuristica_manhattan(inicio, objetivo), inicio, [inicio])]
    visitados = set()

    resultado.addfronteira(1)
    
    while fila_prioridade:
        _, atual, caminho = heapq.heappop(fila_prioridade)

        resultado.addExpandidos(1)
        
        if atual == objetivo:
            resultado.sucesso = True
            resultado.passos = len(caminho)
            resultado.custo = len(caminho) -1
            resultado.finish()

            return caminho, resultado
            
        if atual not in visitados:
            visitados.add(atual)
            
            for vizinho in get_vizinhos(grid, atual):
                if vizinho not in visitados:
                    h = heuristica_manhattan(vizinho, objetivo)
                    heapq.heappush(fila_prioridade, (h, vizinho, caminho + [vizinho]))

                    resultado.addfronteira(1)
    resultado.finish()               
    return None, resultado