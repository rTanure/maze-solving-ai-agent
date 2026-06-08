from multiprocessing import Pool, cpu_count, Manager
from src.utils.verify_missing_results import verify_missing_results
from src.utils.buscas.gerencia_busca import GerenciadorDeBusca
from src.utils.Maze import Maze

def processar_um_labirinto(args_empacotados):
    """
    Processa um único labirinto executando todos os algoritmos faltantes para ele.
    """
    maze_id, missing_algorithms, extra_args, extra_kwargs = args_empacotados
    
    maze = Maze.open(maze_id)
    if maze is None:
        print(f"Labirinto {maze_id} não encontrado. Pulando...")
        return

    buscador = GerenciadorDeBusca()
    
    for algorithm in missing_algorithms:
        # Filtros de segurança por tamanho do labirinto
        tamanho = maze.width * maze.length
        if tamanho > 100000 and algorithm == "ONLINE_A*": continue
        if tamanho > 250000 and algorithm == "DFS": continue

        print(f"[Core] Iniciando: {maze_id} -> {algorithm}")
        
        try:
            # Executa a busca passando o lock adiante via kwargs
            buscador.executar_busca(algorithm, maze, *extra_args, **extra_kwargs)
        except Exception as e:
            print(f"Erro ao executar {algorithm} no labirinto {maze_id}: {e}")
        
        print(f"[Core] Finalizado: {maze_id} -> {algorithm}")


def run_missing_results(missing_results, *args, **kwargs):
    """
    Gerencia a execução paralela dos algoritmos faltantes utilizando um Pool de processos
    e um Lock compartilhado para evitar corrupção de arquivos (Race Conditions).
    """
    if not missing_results:
        print("Nenhum resultado pendente.")
        return

    total_labirintos = len(missing_results)
    num_cores = cpu_count()
    
    print(f"Iniciando processamento paralelo utilizando {num_cores} núcleos para {total_labirintos} labirintos...")

    # Criamos o Manager para gerar um Lock capaz de ser compartilhado entre processos distintos
    with Manager() as manager:
        lock = manager.Lock()
        
        # Injetamos o lock dentro dos kwargs originais para que o backend de salvamento possa usá-lo
        kwargs_com_lock = kwargs.copy()
        kwargs_com_lock['file_lock'] = lock

        # Prepara a lista de tuplas contendo os argumentos de cada processo filho
        tarefas = [
            (maze_id, missing_algorithms, args, kwargs_com_lock) 
            for maze_id, missing_algorithms in missing_results.items()
        ]

        # Dispara o Pool de processos para processar em paralelo
        with Pool(processes=num_cores) as pool:
            pool.map(processar_um_labirinto, tarefas)
    
    print("Resultados finalizados")