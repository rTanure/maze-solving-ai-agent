from src.menus.menu_classicas import menu_classicas

def menu_buscas_geral(labirinto):
    while True:
        print("1. Busca Clássica")
        print("2. Busca Local")
        print("3. Busca Online")
        print("0. Voltar menu anterior")

        option = input("Opção: ").strip()

        if option == '0':
            break

        elif option == '1':
            menu_classicas(labirinto)