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

    # salva os valores originais
    start_original = maze_obj.start
    end_original = maze_obj.end

    for i in range(len(chaves)):
        for j in range(i + 1, len(chaves)):
            origem_id = chaves[i]
            destino_id = chaves[j]

            coord_origem = pontos[origem_id]
            coord_destino = pontos[destino_id]

            maze_obj.start = coord_origem
            maze_obj.end = coord_destino

            resultado = ucs(maze_obj)

            custo = resultado.custo if resultado.sucesso else float('inf')
            caminho = resultado.caminho if resultado.sucesso else []

            matriz[origem_id][destino_id] = custo
            matriz[destino_id][origem_id] = custo

            matriz_caminho[origem_id][destino_id] = caminho
            matriz_caminho[destino_id][origem_id] = caminho[::-1]

    # restaura os valores originais
    maze_obj.start = start_original
    maze_obj.end = end_original

    return matriz, matriz_caminho, pontos

# Mapeia ID do labirinto -> dados do grafo
_CACHE_GRAFOS = {}

def obter_grafo(maze_obj):
    if maze_obj.id in _CACHE_GRAFOS:
        return _CACHE_GRAFOS[maze_obj.id]


    matriz, caminhos, pontos = matriz_distancias(maze_obj)


    _CACHE_GRAFOS[maze_obj.id] = (matriz, caminhos, pontos)

    return matriz, caminhos, pontos