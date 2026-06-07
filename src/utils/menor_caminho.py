from src.utils.buscas.classicas.ucs import ucs

def mapear_pontos(maze_obj):
    pontos = {}

    grid = maze_obj.maze if isinstance(maze_obj.maze, list) else maze_obj.maze.split('\n')
    
    for y, linha in enumerate(grid):
        for x, char in enumerate(linha):
            if char == 'A':
                pontos['A'] = (x, y) 
            elif char == 'B':
                pontos['B'] = (x, y) 
            elif char == 'C': 
                pontos[(x, y)] = (x, y) 
                
    return pontos

def matriz_distancias(maze_obj):
    pontos = mapear_pontos(maze_obj)
    chaves = list(pontos.keys())

    matriz = {k: {} for k in chaves}
    matriz_caminho = {k: {} for k in chaves}

    for i in range(len(chaves)):
        for j in range(i + 1, len(chaves)):
            origem_id = chaves[i]
            destino_id = chaves[j]
            
            coord_origem = pontos[origem_id]
            coord_destino = pontos[destino_id]

            # 1. Em vez de criar uma "maleta", injetamos diretamente no objeto
            # Invertemos aqui pois o UCS vai ler o start/end da matriz usando [y][x]
            maze_obj.start = (coord_origem[1], coord_origem[0])
            maze_obj.end = (coord_destino[1], coord_destino[0])
            
            # 2. Chamada limpa, sem argumentos extras!
            resultado = ucs(maze_obj)
            
            custo = resultado.custo if resultado.sucesso else float('inf')
            caminho = resultado.caminho if resultado.sucesso else []
            
            # Salva o Custo
            matriz[origem_id][destino_id] = custo
            matriz[destino_id][origem_id] = custo
            
            # Salva a Rota
            matriz_caminho[origem_id][destino_id] = caminho
            matriz_caminho[destino_id][origem_id] = caminho[::-1]
            
    return matriz, matriz_caminho, pontos

# Mapeia ID do labirinto -> dados do grafo
_CACHE_GRAFOS = {}

def obter_grafo(maze_obj):
    # Se já calculamos para este labirinto, retorna o cache
    if maze_obj.id in _CACHE_GRAFOS:
        return _CACHE_GRAFOS[maze_obj.id]
    
    # Senão, calcula e salva
    matriz, caminhos, pontos = matriz_distancias(maze_obj)
    _CACHE_GRAFOS[maze_obj.id] = (matriz, caminhos, pontos)
    return matriz, caminhos, pontos