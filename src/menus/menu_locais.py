import questionary

from src.utils.Maze import Maze
from src.utils.buscas.local.hill_climbing import hill_climbing
from src.utils.buscas.local.simulated_annealing import simulated_annealing


def menu_locais():
    algoritmo = questionary.select(
        "Escolha o algoritmo:",
        choices=[
            "Hill Climbing",
            "Simulated Annealing"
        ]
    ).ask()

    temp_inicial = None
    taxa_resfriamento = None

    if algoritmo == "Simulated Annealing":
        temp_inicial = questionary.text(
            "Temperatura inicial (padrão 1000):"
        ).ask()

        taxa_resfriamento = questionary.text(
            "Taxa de resfriamento (padrão 0.99):"
        ).ask()

        temp_inicial = float(temp_inicial) if temp_inicial else 1000
        taxa_resfriamento = (
            float(taxa_resfriamento.replace(",", "."))
            if taxa_resfriamento else 0.99
        )

    mazes = Maze.load_all()

    if not mazes:
        print("Nenhum labirinto encontrado.")
        return

    print(f"\nExecutando em {len(mazes)} labirintos...\n")

    resultados = []

    for maze in mazes:

        print(f"Labirinto {maze.id}")

        if algoritmo == "Hill Climbing":
            resultado = hill_climbing(maze)

        else:
            resultado = simulated_annealing(
                maze,
                temp_inicial,
                taxa_resfriamento
            )

        resultados.append(resultado)

        print(
            f"Custo: {resultado.custo} | "
            f"Tempo: {resultado.tempo:.6f}s"
        )

    print("\nExecução finalizada.")

    return resultados