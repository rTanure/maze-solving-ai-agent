from src.utils.buscas.classicas.ucs import ucs

def mapear_pontos(grid_linhas):
    pontos = {}
    
    for y, linha in enumerate(grid_linhas):
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

            inicio_y_x = (coord_origem[1], coord_origem[0])
            objetivo_y_x = (coord_destino[1], coord_destino[0])

            maleta_override = {
                'inicio_override': inicio_y_x,
                'objetivo_override': objetivo_y_x
            }
            
            resultado = ucs(maze_obj, dados_adicionais=maleta_override)
            
            custo = resultado.custo if resultado.sucesso else float('inf')
            caminho = resultado.caminho if resultado.sucesso else []
            
            # Salva o Custo (ida e volta)
            matriz[origem_id][destino_id] = custo
            matriz[destino_id][origem_id] = custo
            
            # Salva a Rota de Coordenadas
            matriz_caminho[origem_id][destino_id] = caminho
            
            # O Pulo do Gato: O caminho de volta é exatamente a lista invertida!
            # [::-1] inverte a lista no Python para economizarmos processamento.
            matriz_caminho[destino_id][origem_id] = caminho[::-1]
            
    return matriz, matriz_caminho, pontos