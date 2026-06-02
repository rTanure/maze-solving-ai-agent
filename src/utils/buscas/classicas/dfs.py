from utils.auxiliar_busca import get_vizinhos
from utils.resultados.resultado_dfs import ResultadoDFS

def dfs(grid, inicio, objetivo):
    resultado = ResultadoDFS()
    resultado.start()

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
            resultado.finish()

            return caminho, resultado
            
        if atual not in visitados:
            visitados.add(atual)
            
            for vizinho in get_vizinhos(grid, atual):
                if vizinho not in visitados:
                    pilha.append((vizinho, caminho + [vizinho]))
                    resultado.addfronteira(1)
    resultado.finish()                
    return None, resultado