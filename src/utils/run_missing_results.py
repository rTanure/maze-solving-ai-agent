from src.utils.verify_missing_results import verify_missing_results
from src.utils.buscas.gerencia_busca import GerenciadorDeBusca
from src.utils.Maze import Maze

def run_missing_results(missing_results, *args, **kwargs):

    # Calcula o total de buscas que precisam ser executadas
    total_tarefas = sum(len(algorithms) for algorithms in missing_results.values())
    
    if total_tarefas == 0:
        print("Nenhum resultado pendente.")
        return

    buscador = GerenciadorDeBusca()
    progresso_atual = 0

    for maze_id, missing_algorithms in missing_results.items():
        maze = Maze.open(maze_id)

        for algorithm in missing_algorithms:
            progresso_atual += 1
            porcentagem = (progresso_atual / total_tarefas) * 100
            
            # Print formatado: ID - Algoritmo (Progresso/Total - Porcentagem%)
            print(f"{maze_id} - {algorithm} ({progresso_atual}/{total_tarefas} - {porcentagem:.2f}%)")
            
            buscador.executar_busca(algorithm, maze, *args, **kwargs)
            
    
    print("Resultados finalizados")

