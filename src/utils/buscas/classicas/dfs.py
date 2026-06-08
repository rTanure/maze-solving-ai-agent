import time
from src.utils.buscas.auxiliar_busca import get_vizinhos, encontrar_inicio_fim
from src.utils.resultados.resultado_dfs import ResultadoDFS

def dfs(maze_obj):
    resultado = ResultadoDFS(maze_obj.id)
    resultado.start()

    grid = maze_obj.maze
    inicio, objetivo = encontrar_inicio_fim(maze_obj)

    # A pilha agora guarda APENAS a coordenada atual, sem carregar a lista de caminhos
    pilha = [inicio]
    visitados = set()
    
    # Dicionário para reconstruir o caminho de forma leve no final: mapeia filho -> pai
    pais = {inicio: None}
    
    resultado.addfronteira(1)
    
    while pilha:
        atual = pilha.pop()
        resultado.addExpandidos(1)
        
        if atual == objetivo:
            # Reconstrói o caminho de trás para frente apenas UMA vez (no sucesso)
            caminho = []
            passo_atual = objetivo
            while passo_atual is not None:
                caminho.append(passo_atual)
                passo_atual = pais[passo_atual]
            caminho.reverse() # Inverte para ficar do início ao fim
            
            resultado.sucesso = True
            resultado.passos = len(caminho)
            resultado.custo = len(caminho) - 1 
            resultado.caminho = caminho
            resultado.finish()
            return resultado
            
        if atual not in visitados:
            visitados.add(atual)
            
            for vizinho in get_vizinhos(grid, atual):
                if vizinho not in visitados and vizinho not in pilha:
                    # Registra quem é o pai deste vizinho antes de empilhar
                    pais[vizinho] = atual
                    pilha.append(vizinho)
                    resultado.addfronteira(1)
                    
    resultado.finish()                
    return resultado