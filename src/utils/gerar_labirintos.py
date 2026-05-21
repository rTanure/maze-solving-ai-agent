import random
import numpy as np

# Implementação do algoritmo Recursive Backtracking modificado para Braid Maze, permitindo ciclos.
# Características:
#     - Sempre vai existir pelo menos um caminho válido entre todos os pontos do labirinto.
#     - Gera ciclos (múltiplos caminhos possíveis) de forma controlada através da quebra de paredes divisórias.
#     - Ajusta automaticamente dimensões pares para dimensões ímpares para evitar quebra da estrutura de grade.
#     - Distribui pontos de Início (A), Fim (B) e itens de coleta em letras minúsculas (a, b, c...) em posições seguras e alcançáveis.

def gerar_labirinto(largura, altura, num_coletaveis, chance_ciclo=0.1):
    if largura % 2 == 0: largura += 1
    if altura % 2 == 0: altura += 1

    maze = np.ones((altura, largura), dtype=int)

    def get_vizinhos(x, y):
        vizinhos = []
        for dx, dy in [(0, 2), (0, -2), (2, 0), (-2, 0)]:
            nx, ny = x + dx, y + dy
            if 0 < nx < largura - 1 and 0 < ny < altura - 1:
                vizinhos.append((nx, ny))
        return vizinhos

    stack = [(1, 1)]
    maze[1, 1] = 0
    
    while stack:
        x, y = stack[-1]
        vizinhos = [v for v in get_vizinhos(x, y) if maze[v[1], v[0]] == 1]
        
        if vizinhos:
            nx, ny = random.choice(vizinhos)
            maze[y + (ny - y) // 2, x + (nx - x) // 2] = 0
            maze[ny, nx] = 0
            stack.append((nx, ny))
        else:
            stack.pop()

    for y in range(1, altura - 1):
        for x in range(1, largura - 1):
            if maze[y, x] == 1:
                caminho_horizontal = maze[y, x-1] == 0 and maze[y, x+1] == 0 and maze[y-1, x] == 1 and maze[y+1, x] == 1
                caminho_vertical = maze[y-1, x] == 0 and maze[y+1, x] == 0 and maze[y, x-1] == 1 and maze[y, x+1] == 1
                
                if (caminho_horizontal or caminho_vertical) and random.random() < chance_ciclo:
                    maze[y, x] = 0

    inicio_x, inicio_y = 1, 1
    fim_x, fim_y = largura - 2, altura - 2
    
    maze[fim_y, fim_x] = 0
    if maze[fim_y - 1, fim_x] == 1 and maze[fim_y, fim_x - 1] == 1:
        maze[fim_y - 1, fim_x] = 0

    caminhos_livres = list(zip(*np.where(maze == 0)))
    caminhos_livres = [(y, x) for y, x in caminhos_livres if (x, y) != (inicio_x, inicio_y) and (x, y) != (fim_x, fim_y)]
    
    coletaveis_pos = random.sample(caminhos_livres, min(num_coletaveis, len(caminhos_livres)))
    
    matriz_final = np.full((altura, largura), '#', dtype=str)
    matriz_final[maze == 0] = ' '
    matriz_final[inicio_y, inicio_x] = 'A'
    matriz_final[fim_y, fim_x] = 'B'
    
    for i, (y, x) in enumerate(coletaveis_pos):
        matriz_final[y, x] = chr(97 + i)
        
    return "\n".join(["".join(linha) for linha in matriz_final])