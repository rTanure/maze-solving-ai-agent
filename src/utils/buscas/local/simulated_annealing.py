import math
import random

from src.utils.resultados.resultado_simulated_annealing import ResultadoSimulatedAnnealing
from src.utils.buscas.local.hill_climbing import (
    calcular_custo_rota,
    gerar_vizinhos_por_troca
)


def simulated_annealing(maze_obj, temp_inicial, taxa_resfriamento):

    if taxa_resfriamento <= 0 or taxa_resfriamento >= 1:
        raise ValueError(
            f"Taxa de resfriamento inválida: {taxa_resfriamento}. "
            "Ela deve estar entre 0 e 1."
        )


    resultado = ResultadoSimulatedAnnealing(maze_obj.id)
    resultado.start()

    from src.utils.menor_caminho import obter_grafo

    matriz_distancias, matriz_caminhos, pontos = obter_grafo(maze_obj)


    lista_coletaveis = [
        k for k in pontos.keys()
        if isinstance(k, tuple)
    ]


    if len(lista_coletaveis) <= 1:


        custo = calcular_custo_rota(
            lista_coletaveis,
            matriz_distancias
        )

        resultado.finish()

        resultado.sucesso = True
        resultado.custo = custo
        resultado.passos = 0
        resultado.iteracoes = 0
        resultado.curva = [(0, custo)]

        resultado.ordem_coletaveis = lista_coletaveis

        rota_macro = ['A'] + lista_coletaveis + ['B']
        resultado.rota_macro = rota_macro

        if matriz_caminhos:

            caminho_completo = []

            for i in range(len(rota_macro) - 1):

                origem = rota_macro[i]
                destino = rota_macro[i + 1]

                trecho = matriz_caminhos[origem][destino]

                if i > 0 and len(trecho) > 0:
                    trecho = trecho[1:]

                caminho_completo.extend(trecho)

            resultado.caminho = caminho_completo

        else:
            resultado.caminho = rota_macro

        return resultado


    estado_atual = lista_coletaveis[:]
    random.shuffle(estado_atual)


    custo_atual = calcular_custo_rota(
        estado_atual,
        matriz_distancias
    )


    melhor_estado = estado_atual[:]
    melhor_custo = custo_atual

    temp = temp_inicial

    iteracoes = 0
    curva_convergencia = [(0, custo_atual)]


    while temp > 0.1:

        iteracoes += 1

        if iteracoes % 1000 == 0:
            print(
                f"Iteração {iteracoes} | "
                f"Temp={temp:.4f} | "
                f"Melhor={melhor_custo}"
            )

        vizinhos = gerar_vizinhos_por_troca(
            estado_atual
        )

        if not vizinhos:
            print("Sem vizinhos")
            break

        candidato = random.choice(vizinhos)

        custo_candidato = calcular_custo_rota(
            candidato,
            matriz_distancias
        )

        delta = custo_candidato - custo_atual


        if (
            delta < 0
            or random.random() < math.exp(-delta / temp)
        ):

            estado_atual = candidato
            custo_atual = custo_candidato

            if custo_atual < melhor_custo:

                melhor_estado = estado_atual[:]
                melhor_custo = custo_atual

                
        curva_convergencia.append((iteracoes, custo_atual))
        temp *= taxa_resfriamento


    resultado.finish()

    resultado.sucesso = True
    resultado.custo = melhor_custo
    resultado.passos = iteracoes
    resultado.iteracoes = iteracoes
    resultado.curva = curva_convergencia

    resultado.ordem_coletaveis = melhor_estado

    rota_macro = ['A'] + melhor_estado + ['B']
    resultado.rota_macro = rota_macro


    if matriz_caminhos:

        caminho_completo = []

        for i in range(len(rota_macro) - 1):

            origem = rota_macro[i]
            destino = rota_macro[i + 1]


            trecho = matriz_caminhos[origem][destino]

            if i > 0 and len(trecho) > 0:
                trecho = trecho[1:]

            caminho_completo.extend(trecho)

        resultado.caminho = caminho_completo

    else:
        resultado.caminho = rota_macro


    return resultado