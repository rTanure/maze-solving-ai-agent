# Importações das Buscas Clássicas e Online
from src.utils.resultados.resultado_bfs import ResultadoBFS
from src.utils.resultados.resultado_dfs import ResultadoDFS
from src.utils.resultados.resultado_ucs import ResultadoUCS
from src.utils.resultados.resultado_guloso import ResultadoGuloso
from src.utils.resultados.resultado_a_star import ResultadoAStar
from src.utils.resultados.resultado_online_a_star import ResultadoOnlineAStar
from src.utils.resultados.resultado_simulated_annealing import ResultadoSimulatedAnnealing

from src.utils.buscas.classicas.bfs import bfs
from src.utils.buscas.classicas.dfs import dfs
from src.utils.buscas.classicas.ucs import ucs
from src.utils.buscas.classicas.greedy import busca_gulosa
from src.utils.buscas.classicas.a_star import a_star
from src.utils.buscas.online.online_a_star import online_a_star

# Importação da Busca Local (Hill Climbing)
from src.utils.resultados.resultado_hill_climbing import ResultadoHillClimbing
from src.utils.buscas.local.hill_climbing import hill_climbing
from src.utils.buscas.local.simulated_annealing import simulated_annealing
from src.utils.buscas.local.simulated_annealing_iteracoes import rodar_bateria_simulated_annealing
from src.utils.buscas.local.hill_climbing_iteracoes import rodar_bateria_hill_climbing

class GerenciadorDeBusca:
    def __init__(self):
        self.algoritmos = {
            'BFS': {'funcao': bfs, 'classe_resultado': ResultadoBFS},
            'DFS': {'funcao': dfs, 'classe_resultado': ResultadoDFS},
            'UCS': {'funcao': ucs, 'classe_resultado': ResultadoUCS},
            'GULOSA': {'funcao': busca_gulosa, 'classe_resultado': ResultadoGuloso},
            'ASTAR': {'funcao': a_star, 'classe_resultado': ResultadoAStar},
            'ONLINE_A*': {'funcao': online_a_star, 'classe_resultado': ResultadoOnlineAStar},
            'HILL_CLIMBING': {'funcao': hill_climbing, 'classe_resultado': ResultadoHillClimbing},
            'SIMULATED_ANNEALING': {'funcao': simulated_annealing, 'classe_resultado': ResultadoSimulatedAnnealing}
        }

    def executar_busca(self, nome_algoritmo, maze_obj, *args, **kwargs):
        
        nome_algoritmo = nome_algoritmo.upper()
        
        if nome_algoritmo not in self.algoritmos:
            raise ValueError(f"Algoritmo '{nome_algoritmo}' não suportado. Opções válidas: {list(self.algoritmos.keys())}")

        file_lock = kwargs.pop('file_lock', None)

        referencia = self.algoritmos[nome_algoritmo]
        funcao_busca = referencia['funcao']

        
        # 2. CHAMADA NOVA: Passa só o objeto e recebe só o relatório de volta
        match nome_algoritmo:
            case "HILL_CLIMBING":
                # Se não informarem num_execucoes, o padrão será 100
                num_execucoes = kwargs.get('num_execucoes', 100) 
                relatorios = []
                for _ in range(num_execucoes):
                    relatorios.append(funcao_busca(maze_obj))
                
            case "SIMULATED_ANNEALING":
                num_execucoes = kwargs.get('num_execucoes')
                temp_inicial = kwargs.get('temp_inicial')
                taxa_resfriamento = kwargs.get('taxa_resfriamento')

                relatorios = []
                for _ in range(num_execucoes):
                    relatorios.append(funcao_busca(maze_obj, temp_inicial=temp_inicial, taxa_resfriamento=taxa_resfriamento))
                
            case _:
                relatorios = [funcao_busca(maze_obj)]
        
        # 3. SALVAR RESULTADO COM ID INTELIGENTE
        if file_lock is not None:
            with file_lock:
                for relatorio in relatorios: 
                    relatorio.salvarResultado()
        else:
            for relatorio in relatorios: 
                relatorio.salvarResultado()