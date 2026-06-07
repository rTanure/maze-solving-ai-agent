from src.utils.Maze import Maze

from src.utils.resultados.resultado_ucs import ResultadoUCS
from src.utils.resultados.resultado_bfs import ResultadoBFS
from src.utils.resultados.resultado_a_star import ResultadoAStar
from src.utils.resultados.resultado_guloso import ResultadoGuloso
from src.utils.resultados.resultado_dfs import ResultadoDFS

def verify_missing_results():
    ids_totais = Maze.get_ids()

    # Mapeamento dos métodos e suas respectivas classes de resultado
    metodos_busca = {
        "UCS": ResultadoUCS,
        "DFS": ResultadoDFS,
        "BFS": ResultadoBFS,
        "GULOSA": ResultadoGuloso,
        "ASTART": ResultadoAStar,
        "ONLINE_ASTAR": ResultadoAStar
    }

    ids_por_metodo = {}

    # 1. Coleta os IDs existentes apenas de DataFrames válidos e populados
    for nome_metodo, classe_resultado in metodos_busca.items():
        try:
            df_resultado = classe_resultado.get_df()
            
            # Se o df existir, não estiver vazio e contiver a coluna, extrai os IDs
            if df_resultado is not None and not df_resultado.empty and "maze_id" in df_resultado.columns:
                ids_por_metodo[nome_metodo] = set(df_resultado["maze_id"].astype(str).values)
            else:
                # Se cair aqui (vazio/inexistente), assume conjunto vazio (falta em todos)
                ids_por_metodo[nome_metodo] = set()
                
        except Exception:
            # Qualquer erro na leitura também assume que o método falta em todos
            ids_por_metodo[nome_metodo] = set()

    # 2. Constrói o mapa de pendências
    relatorio_faltantes = {}

    for id_labirinto in ids_totais:
        id_labirinto_str = str(id_labirinto)
        metodos_faltantes = []

        for nome_metodo in metodos_busca.keys():
            # Se o conjunto estiver vazio ou o ID não estiver lá, entra como faltante
            if id_labirinto_str not in ids_por_metodo[nome_metodo]:
                metodos_faltantes.append(nome_metodo)

        # Adiciona ao relatório se houver alguma pendência para o labirinto
        if metodos_faltantes:
            relatorio_faltantes[id_labirinto_str] = metodos_faltantes

    return relatorio_faltantes