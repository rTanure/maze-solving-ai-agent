import questionary
from src.utils.validadores import *
from src.utils.os_utils import limpar_terminal
from src.menus.menu_gerador import menu_gerar_labirintos_lotes
from src.menus.menu_results import menu_results
from src.menus.menu_simulacao import menu_simulacao_temporaria


def menu_principal():
  limpar_terminal()
  
  # O dicionário agora guarda funções normais ou lambdas que retornam um booleano (True para sair)
  choices = {
    "Gerar em lote": lambda: (menu_gerar_labirintos_lotes(), False)[1],
    "Simular labirinto temporario": lambda: (menu_simulacao_temporaria(), False)[1],
    "Executar exprimentos": lambda: (menu_results(), False)[1],
    "Resolver o labirinto": lambda: (print("Escolheu resolver o labirinto"), False)[1],
    "Sair": lambda: True  # Retorna True indicando que deve sair
  }

  escolha = questionary.select("Escolha uma opção:", choices=list(choices.keys())).ask()

  # Executa a ação e armazena se o usuário pediu para sair ou não
  deve_sair = choices.get(escolha, lambda: False)()
  
  # Se não pediu para sair, continua o menu. Se pediu, a função termina aqui.
  if not deve_sair: 
    menu_principal()
