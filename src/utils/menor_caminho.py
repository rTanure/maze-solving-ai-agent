from src.utils.buscas.classicas.ucs import ucs

def mapear_pontos(linhas):
    pontos = {}
    contador_coletaveis = 1

    for y, linha in enumerate(linhas):
        for x, char in enumerate(linha):
            if char == 'A':
                pontos['A'] = (y, x)
            elif char == 'B':
                pontos['B'] = (y, x)
            elif char == 'C':
                coletavel = f'C{contador_coletaveis}'
                pontos[coletavel] = (y, x)
                contador_coletaveis += 1
    
    return pontos

def matriz_distancias(linhas):
    pontos = mapear_pontos(linhas)
    chaves = list(pontos.keys())

    matriz = {k: {} for k in chaves}

    calculados = 0

    for i in range(len(chaves)):
        for j in range(i + 1, len(chaves)):
            origem_id = chaves[i]
            destino_id = chaves[j]
            
            coord_origem = pontos[origem_id]
            coord_destino = pontos[destino_id]
            
            _, resultado = ucs(linhas, coord_origem, coord_destino)
            
            custo = resultado.custo if resultado.sucesso else float('inf')
            
            matriz[origem_id][destino_id] = custo
            matriz[destino_id][origem_id] = custo
            
            calculados += 1
            
    return matriz, pontos