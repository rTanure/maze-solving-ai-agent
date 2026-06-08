from src.utils.Maze import Maze

from src.utils.resultados.resultado_ucs import ResultadoUCS
from src.utils.resultados.resultado_bfs import ResultadoBFS
from src.utils.resultados.resultado_a_star import ResultadoAStar
from src.utils.buscas.online.online_a_star import ResultadoOnlineAStar
from src.utils.resultados.resultado_guloso import ResultadoGuloso
from src.utils.resultados.resultado_dfs import ResultadoDFS
from src.utils.resultados.resultado_simulated_annealing import ResultadoSimulatedAnnealing
from src.utils.resultados.resultado_hill_climbing import ResultadoHillClimbing


def verify_missing_results() -> dict[str, list[str]]:
    ids_totais = {str(id_).strip().lower() for id_ in Maze.get_ids()}


    metodos_busca = {
        "UCS": ResultadoUCS,
        "DFS": ResultadoDFS,
        "BFS": ResultadoBFS,
        "GULOSA": ResultadoGuloso,
        "ASTAR": ResultadoAStar,
        "ONLINE_A*": ResultadoOnlineAStar,
        "SIMULATED_ANNEALING": ResultadoSimulatedAnnealing,
        "HILL_CLIMBING": ResultadoHillClimbing,
    }

    ids_por_metodo = {}
    

    for nome_metodo, classe_resultado in metodos_busca.items():
        try:
            df_resultado = classe_resultado.get_df()
            
            if df_resultado is not None and not df_resultado.empty and "maze_id" in df_resultado.columns:
                # Padronização para UUIDs:
                # 1. Remove linhas nulas (.dropna)
                # 2. Transforma tudo em string (.astype(str))
                # 3. Remove espaços e força minúsculo (.str.strip().str.lower())
                ids_existentes = (
                    df_resultado["maze_id"]
                    .dropna()
                    .astype(str)
                    .str.strip()
                    .str.lower()
                    .values
                )
                ids_por_metodo[nome_metodo] = set(ids_existentes)
            else:
                ids_por_metodo[nome_metodo] = set()
                
        except Exception:
            ids_por_metodo[nome_metodo] = set()


    # Monta o relatório final comparando os UUIDs padronizados
    relatorio_faltantes = {}
    
    for id_labirinto in ids_totais:
        metodos_faltantes = [
            nome_metodo 
            for nome_metodo, ids_salvos in ids_por_metodo.items() 
            if id_labirinto not in ids_salvos
        ]
        
        if metodos_faltantes:
            relatorio_faltantes[id_labirinto] = metodos_faltantes
    return relatorio_faltantes