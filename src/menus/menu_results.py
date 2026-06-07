import questionary

from src.utils.verify_missing_results import verify_missing_results
from src.utils.run_missing_results import run_missing_results

def menu_results():
    missing_results = verify_missing_results()
    temp_inicial = None
    taxa_resfriamento = None
    num_execucoes = None

    algorithm_set = set()
    for _, v in missing_results.items():
        for algorithm in v:
            algorithm_set.add(algorithm)

    print(algorithm_set)

    if "SIMULATED_ANNEALING" in algorithm_set or "HILL_CLIMBING" in algorithm_set:
        num_execucoes_str = questionary.text("Numero de execucoes (padrão 100):").ask()
        num_execucoes = int(num_execucoes_str) if num_execucoes_str else 100

    if "SIMULATED_ANNEALING" in algorithm_set:
        temp_inicial_str = questionary.text("Temperadura inicial do simulated annealing (padrão 1000):").ask()
        taxa_resfriamento_str = questionary.text("Taxa de resfriamento do simulated annealing (padrão 3):").ask()
        temp_inicial = int(temp_inicial_str) if temp_inicial_str else 1000
        taxa_resfriamento = (
            float(taxa_resfriamento_str)
            if taxa_resfriamento_str
            else 0.95
        )

    run_missing_results(
        missing_results = missing_results,
        temp_inicial = temp_inicial,
        taxa_resfriamento = taxa_resfriamento,
        num_execucoes = num_execucoes
    )
