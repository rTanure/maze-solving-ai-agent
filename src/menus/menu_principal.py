import questionary
from src.utils.validadores import *
from src.utils.os_utils import limpar_terminal
from src.menus.menu_gerador import menu_gerar_labirintos_lotes


def menu_principal():
  limpar_terminal()
  choices = {
    "Gerar labirinto": lambda: print("TODO"),
    "Gerar em lote": lambda: menu_gerar_labirintos_lotes(),
    "Resolver o labirinto": lambda: print("Escolheu resolver o labirinto"),
    "Sair": lambda: print("Saindo do programa...")
  }

  escolha = questionary.select("Escolha uma opção:", choices=list(choices.keys())).ask()

  choices.get(escolha, lambda: print("Opção inválida"))()