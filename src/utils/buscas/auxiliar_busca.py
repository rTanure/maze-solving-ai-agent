import heapq
from collections import deque

def get_celula(grid, coord):
    x, y = coord
    return grid[y][x]

def parse_labirinto(labirinto_str):
    grid = [list(linha) for linha in labirinto_str.strip().split('\n')]
    inicio = None
    objetivo = None
    
    for y, linha in enumerate(grid):
        for x, char in enumerate(linha):
            if char == 'A':
                inicio = (x, y)
            elif char == 'B':
                objetivo = (x, y)
                
    return grid, inicio, objetivo

def get_vizinhos(grid, no):
    x, y = no
    vizinhos = []
    direcoes = [(-1, 0), (1, 0), (0, -1), (0, 1)] 
    
    for dx, dy in direcoes:
        nx, ny = x + dx, y + dy
        if 0 <= ny < len(grid) and 0 <= nx < len(grid[0]):
            if grid[ny][nx] != '#':
                vizinhos.append((nx, ny))
    return vizinhos

def heuristica_manhattan(no1, no2):
    return abs(no1[0] - no2[0]) + abs(no1[1] - no2[1])

def encontrar_inicio_fim(maze_obj):
    # Extrai o X e Y da tupla que veio do Maze
    start_x, start_y = maze_obj.start
    end_x, end_y = maze_obj.end
    
    # Retorna invertido (y, x) para os algoritmos usarem na grid
    return (start_y, start_x), (end_y, end_x)