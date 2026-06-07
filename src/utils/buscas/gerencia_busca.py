from src.utils.auxiliar_busca import parse_labirinto
from src.utils.resultados.resultado_bfs import ResultadoBFS
from src.utils.resultados.resultado_dfs import ResultadoDFS
from src.utils.resultados.resultado_ucs import ResultadoUCS
from src.utils.resultados.resultado_guloso import ResultadoGuloso
from src.utils.resultados.resultado_a_star import ResultadoAStar

from src.utils.buscas.classicas.bfs import bfs
from src.utils.buscas.classicas.dfs import dfs
from src.utils.buscas.classicas.ucs import ucs
from src.utils.buscas.classicas.greedy import busca_gulosa
from src.utils.buscas.classicas.a_star import a_star

class GerenciadorDeBusca:
    def __init__(self):
        self.algoritmos = {
            'BFS': {'funcao': bfs, 'classe_resultado': ResultadoBFS},
            'DFS': {'funcao': dfs, 'classe_resultado': ResultadoDFS},
            'UCS': {'funcao': ucs, 'classe_resultado': ResultadoUCS},
            'GULOSA': {'funcao': busca_gulosa, 'classe_resultado': ResultadoGuloso}
            'A*': {'funcao': a_star, 'classe_resultado': ResultadoAStar}
            'ONLINE_A*': {'funcao': online_a_star, 'classe_resultado': ResultadoOnlineAStar}
        }

    def executar_busca(self, nome_algoritmo, labirinto_str, dados_adicionais=None):
        
        nome_algoritmo = nome_algoritmo.upper()
        
        if nome_algoritmo not in self.algoritmos:
            raise ValueError(f"Algoritmo '{nome_algoritmo}' não suportado. Opções válidas: {list(self.algoritmos.keys())}")
            
        if dados_adicionais is None:
            dados_adicionais = {}

        grid, inicio, objetivo = parse_labirinto(labirinto_str)
        
        if not inicio or not objetivo:
            print(f"Erro: Labirinto inválido para {nome_algoritmo}. Pontos A e/ou B não encontrados.")
            return None, None

        referencia = self.algoritmos[nome_algoritmo]
        funcao_busca = referencia['funcao']

        print(f"\n--- Iniciando execução: {nome_algoritmo} ---")
        
        caminho, relatorio = funcao_busca(grid, inicio, objetivo)

        if relatorio.sucesso:
            print(f"[{nome_algoritmo}] Caminho encontrado! (Passos: {relatorio.passos}, Custo: {relatorio.custo})")
        else:
            print(f"[{nome_algoritmo}] Falha. Nenhum caminho encontrado.")
            
        if hasattr(relatorio, '_salvaResultado'):
             relatorio.salvarResultado()
             print(f"[{nome_algoritmo}] Resultados salvos com sucesso.")

        return caminho, relatorio