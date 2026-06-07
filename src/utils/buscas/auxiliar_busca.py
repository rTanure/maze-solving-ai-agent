import heapq
from collections import deque

def parse_labirinto(labirinto_str):
    grid = [list(linha) for linha in labirinto_str.strip().split('\n')]
    inicio = None
    objetivo = None
    
    for y, linha in enumerate(grid):
        for x, char in enumerate(linha):
            if char == 'A':
                inicio = (y, x)
            elif char == 'B':
                objetivo = (y, x)
                
    return grid, inicio, objetivo

def get_vizinhos(grid, no):
    y, x = no
    vizinhos = []
    direcoes = [(-1, 0), (1, 0), (0, -1), (0, 1)] 
    
    for dy, dx in direcoes:
        ny, nx = y + dy, x + dx
        if 0 <= ny < len(grid) and 0 <= nx < len(grid[0]):
            if grid[ny][nx] != '#':
                vizinhos.append((ny, nx))
    return vizinhos

def heuristica_manhattan(no1, no2):
    return abs(no1[0] - no2[0]) + abs(no1[1] - no2[1])

def encontrar_inicio_fim(grid):
    inicio = None
    objetivo = None
    for y, linha in enumerate(grid):
        for x, char in enumerate(linha):
            if char == 'A': inicio = (y, x)
            elif char == 'B': objetivo = (y, x)
    return inicio, objetivo