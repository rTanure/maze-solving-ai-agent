import questionary

def menu_principal():
  escolha = questionary.select(
    "Escolha uma opção:",
    choices=["Resolver o labirinto", "Sair"]
  ).ask()

  print(escolha)