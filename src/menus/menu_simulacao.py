import time

import questionary

from src.utils.Maze import Maze
from src.utils.os_utils import limpar_terminal
from src.utils.buscas.classicas.bfs import bfs
from src.utils.buscas.classicas.dfs import dfs
from src.utils.buscas.classicas.ucs import ucs
from src.utils.buscas.classicas.greedy import busca_gulosa
from src.utils.buscas.classicas.a_star import a_star
from src.utils.buscas.online.online_a_star import online_a_star
from src.utils.buscas.local.hill_climbing import hill_climbing
from src.utils.buscas.local.simulated_annealing import simulated_annealing


ALGORITMOS = {
    "BFS": bfs,
    "DFS": dfs,
    "UCS": ucs,
    "Gulosa": busca_gulosa,
    "A*": a_star,
    "Online A*": online_a_star,
    "Hill Climbing": hill_climbing,
    "Simulated Annealing": simulated_annealing,
}

ALGORITMOS_COM_COLETAVEIS = {"Hill Climbing", "Simulated Annealing"}


def _ler_inteiro(mensagem, padrao, minimo=None):
    valor = questionary.text(f"{mensagem} (padrao {padrao}):").ask()
    if not valor:
        return padrao

    try:
        valor_int = int(valor)
    except ValueError:
        print(f"Valor invalido. Usando padrao {padrao}.")
        return padrao

    if minimo is not None and valor_int < minimo:
        return minimo
    return valor_int


def _ler_float(mensagem, padrao, minimo=None, maximo=None):
    valor = questionary.text(f"{mensagem} (padrao {padrao}):").ask()
    if not valor:
        return padrao

    try:
        valor_float = float(valor.replace(",", "."))
    except ValueError:
        print(f"Valor invalido. Usando padrao {padrao}.")
        return padrao

    if minimo is not None and valor_float < minimo:
        return minimo
    if maximo is not None and valor_float > maximo:
        return maximo
    return valor_float


def _revelar_vizinhanca(posicao, altura, largura, reveladas, raio=1):
    x, y = posicao
    for dy in range(-raio, raio + 1):
        for dx in range(-raio, raio + 1):
            if abs(dx) + abs(dy) > raio:
                continue

            nx, ny = x + dx, y + dy
            if 0 <= ny < altura and 0 <= nx < largura:
                reveladas.add((nx, ny))


def _renderizar_frame(grid, caminho, indice_atual, reveladas):
    atual = caminho[indice_atual]
    percorridas = set(caminho[:indice_atual])
    linhas = []

    for y, linha in enumerate(grid):
        chars = []
        for x, celula in enumerate(linha):
            coord = (x, y)

            if coord == atual:
                chars.append("@")
            elif coord in percorridas:
                chars.append(".")
            elif coord not in reveladas:
                chars.append("?")
            else:
                chars.append(celula)

        linhas.append("".join(chars))

    return "\n".join(linhas)


def _maze_tratando_coletaveis_como_livres(maze):
    grid = [
        [" " if celula == "C" else celula for celula in linha]
        for linha in maze.maze
    ]

    return Maze(
        width=maze.width,
        length=maze.length,
        collectibles=0,
        cicles=maze.cicles,
        maze=grid,
        start=maze.start,
        end=maze.end,
        id=maze.id,
    )


def animar_resultado(maze, resultado, algoritmo, atraso=0.08, raio_percepcao=1):
    caminho = list(getattr(resultado, "caminho", []) or [])
    if not caminho:
        print("O algoritmo nao retornou caminho para simular.")
        return

    grid = maze.maze
    altura = len(grid)
    largura = len(grid[0]) if altura else 0
    usa_mapa_desconhecido = algoritmo == "Online A*"
    if usa_mapa_desconhecido:
        reveladas = set()
    else:
        reveladas = {
            (x, y)
            for y in range(altura)
            for x in range(largura)
        }

    for indice, posicao in enumerate(caminho):
        if usa_mapa_desconhecido:
            _revelar_vizinhanca(posicao, altura, largura, reveladas, raio_percepcao)

        limpar_terminal()
        print(f"Simulacao: {algoritmo}")
        print(
            f"Passo {indice}/{len(caminho) - 1} | "
            f"Custo: {getattr(resultado, 'custo', 0)} | "
            f"Expandidos: {getattr(resultado, 'expandidos', 0)}"
        )

        if hasattr(resultado, "replanejamentos"):
            print(
                f"Replanejamentos: {resultado.replanejamentos} | "
                f"Reveladas: {resultado.celulas_reveladas} | "
                f"Revisitadas: {resultado.celulas_revisitadas}"
            )

        print()
        print(_renderizar_frame(grid, caminho, indice, reveladas))
        time.sleep(atraso)

    print()
    print(
        "Resultado: "
        f"{'sucesso' if getattr(resultado, 'sucesso', False) else 'falha'} | "
        f"passos={getattr(resultado, 'passos', 0)} | "
        f"tempo={getattr(resultado, 'tempo', 0):.6f}s"
    )
    input("Pressione Enter para voltar ao menu...")


def _executar_algoritmo(nome_algoritmo, maze):
    if nome_algoritmo == "Simulated Annealing":
        temp_inicial = _ler_float("Temperatura inicial", 1000, minimo=0.1)
        taxa_resfriamento = _ler_float(
            "Taxa de resfriamento", 0.95, minimo=0.01, maximo=0.99
        )
        return simulated_annealing(
            maze,
            temp_inicial=temp_inicial,
            taxa_resfriamento=taxa_resfriamento,
        )

    return ALGORITMOS[nome_algoritmo](maze)


def menu_simulacao_temporaria():
    limpar_terminal()
    print("Criar labirinto temporario para simulacao\n")

    largura = _ler_inteiro("Largura", 21, minimo=5)
    altura = _ler_inteiro("Altura", 11, minimo=5)
    coletaveis = _ler_inteiro("Quantidade de pontos de coleta", 3, minimo=0)
    ciclos = _ler_float("Probabilidade de ciclos", 0.15, minimo=0.0, maximo=1.0)
    atraso = _ler_float("Atraso entre passos em segundos", 0.08, minimo=0.0)
    maze = Maze.create(
        width=largura,
        height=altura,
        collectibles=coletaveis,
        cicles=ciclos,
    )

    algoritmo = questionary.select(
        "Escolha o metodo de solucao:",
        choices=list(ALGORITMOS.keys()),
    ).ask()

    if not algoritmo:
        return

    raio_percepcao = 1
    if algoritmo == "Online A*":
        raio_percepcao = _ler_inteiro("Raio de percepcao da simulacao", 1, minimo=0)

    if algoritmo not in ALGORITMOS_COM_COLETAVEIS:
        maze = _maze_tratando_coletaveis_como_livres(maze)

    limpar_terminal()
    print(f"Executando {algoritmo}. Aguarde...")
    resultado = _executar_algoritmo(algoritmo, maze)

    animar_resultado(
        maze,
        resultado,
        algoritmo,
        atraso=atraso,
        raio_percepcao=raio_percepcao,
    )
