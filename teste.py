# from src.utils.resultados.resultado_a_star import ResultadoAStar
# import time

# resultado = ResultadoAStar()

# resultado.start()

# resultado.addCusto()
# resultado.addCusto()
# resultado.addCusto()
# resultado.addCusto()
# resultado.addCusto()

# resultado.addExpandidos()
# resultado.addExpandidos()
# resultado.addExpandidos()

# resultado.addPassos()
# resultado.addPassos()

# resultado.addfronteira()

# time.sleep(0.2)

# resultado.finish()

# resultado.salvarResultado()

# teste_gerenciador.py

from src.utils.buscas.gerencia_busca import GerenciadorDeBusca

# Criamos um labirinto minúsculo e previsível na mão só para o teste.
labirinto_teste = """
#######
#A    #
### ###
#    B#
#######
""".strip()

def rodar_testes():
    print("Iniciando testes do Gerenciador de Buscas...")

    # Instancia o gerenciador
    gerenciador = GerenciadorDeBusca()

    # Executa as buscas
    print("\n--- Testando BFS ---")
    caminho_bfs, stats_bfs = gerenciador.executar_busca('BFS', labirinto_teste)

    print("\n--- Testando GULOSA ---")
    caminho_gulosa, stats_gulosa = gerenciador.executar_busca('GULOSA', labirinto_teste)

    # Verifica se a ponte funcionou
    if caminho_bfs and caminho_gulosa:
        print("\n✅ Sucesso! Os algoritmos devolveram o caminho e o relatório.")
        print(f"O BFS expandiu {stats_bfs.expandidos} nós.")
        print(f"A Busca Gulosa expandiu {stats_gulosa.expandidos} nós.")
        print("Verifique sua pasta de datasets para ver se os CSVs foram gerados!")
    else:
        print("\n❌ Algo deu errado. Os caminhos voltaram vazios.")

if __name__ == "__main__":
    rodar_testes()