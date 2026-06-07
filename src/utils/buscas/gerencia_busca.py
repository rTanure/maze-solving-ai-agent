from src.utils.resultados.resultado_bfs import ResultadoBFS
from src.utils.resultados.resultado_dfs import ResultadoDFS
from src.utils.resultados.resultado_ucs import ResultadoUCS
from src.utils.resultados.resultado_guloso import ResultadoGuloso
from src.utils.resultados.resultado_a_star import ResultadoAStar
from src.utils.resultados.resultado_online_a_star import ResultadoOnlineAStar

from src.utils.buscas.classicas.bfs import bfs
from src.utils.buscas.classicas.dfs import dfs
from src.utils.buscas.classicas.ucs import ucs
from src.utils.buscas.classicas.greedy import busca_gulosa
from src.utils.buscas.classicas.a_star import a_star
from src.utils.buscas.online.online_a_star import online_a_star

class GerenciadorDeBusca:
    def __init__(self):
        self.algoritmos = {
            'BFS': {'funcao': bfs, 'classe_resultado': ResultadoBFS},
            'DFS': {'funcao': dfs, 'classe_resultado': ResultadoDFS},
            'UCS': {'funcao': ucs, 'classe_resultado': ResultadoUCS},
            'GULOSA': {'funcao': busca_gulosa, 'classe_resultado': ResultadoGuloso},
            'ASTAR': {'funcao': a_star, 'classe_resultado': ResultadoAStar}, # Ajuste para ASTAR se os lambdas enviam assim
            'ONLINE_ASTAR': {'funcao': online_a_star, 'classe_resultado': ResultadoOnlineAStar}
        }

    # 1. ASSINATURA NOVA: Agora recebe diretamente o objeto Maze!
    def executar_busca(self, nome_algoritmo, maze_obj, dados_adicionais=None):
        
        nome_algoritmo = nome_algoritmo.upper()
        
        if nome_algoritmo not in self.algoritmos:
            raise ValueError(f"Algoritmo '{nome_algoritmo}' não suportado. Opções válidas: {list(self.algoritmos.keys())}")

        referencia = self.algoritmos[nome_algoritmo]
        funcao_busca = referencia['funcao']

        print(f"\n--- Iniciando execução: {nome_algoritmo} ---")
        
        # 2. CHAMADA NOVA: Passa só o objeto e recebe só o relatório de volta
        relatorio = funcao_busca(maze_obj)
        print(relatorio.caminho)
        
        # Extrai o caminho de dentro do relatório (caso o menu precise para desenhar)
        caminho = getattr(relatorio, 'caminho', None)

        if relatorio.sucesso:
            print(f"[{nome_algoritmo}] Caminho encontrado! (Passos: {relatorio.passos}, Custo: {relatorio.custo})")
        else:
            print(f"[{nome_algoritmo}] Falha. Nenhum caminho encontrado.")
            
        # Corrigindo a verificação de método (usando 'salvarResultado' em vez de '_salvaResultado' que estava no seu código)
        if hasattr(relatorio, 'salvarResultado'):
             relatorio.salvarResultado()
             print(f"[{nome_algoritmo}] Resultados salvos no CSV com sucesso.")

        relatorio.caminho = caminho

        return relatorio