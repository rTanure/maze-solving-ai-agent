from src.utils.buscas.gerencia_busca import GerenciadorDeBusca

def menu_classicas(labirinto):
    gerenciador = GerenciadorDeBusca()

    mapa_algoritmos = {
        '1': 'BFS',
        '2': 'DFS',
        '3': 'UCS',
        '4': 'GULOSA',
        '5': 'ASTAR'
    }

    while True:
        print("1. Busca em Largura (BFS)")
        print("2. Busca em Profundidade (DFS)")
        print("3. Busca de Custo Uniforme (UCS)")
        print("4. Busca Gulosa (Greedy)")
        print("5. Busca A* (A-Star)")
        print("9. Executar TODAS as clássicas")
        print("0. Voltar ao Menu Anterior")

        option = input("Opção: ").strip()

        if option == '0':
            break
        elif option in mapa_algoritmos:
            nome_busca = mapa_algoritmos[option]
            gerenciador.executar_busca(nome_busca, labirinto)
        elif option == '9':
            for alg in mapa_algoritmos.values():
                try:
                    gerenciador.executar_busca(alg, labirinto)
                except ValueError:
                    pass
        else:
            print("Inválido")