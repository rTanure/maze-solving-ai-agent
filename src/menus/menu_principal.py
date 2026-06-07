import questionary
from src.utils.gerar_labirintos import gerar_labirinto
from src.utils.validadores import *
from src.utils.os_utils import limpar_terminal
from src.menus.menu_gerador import menu_gerar_labirintos_lotes


def fluxo_gerador():
    """Coleta os parâmetros aceitando inputs vazios como valores padrão."""
    
    w_str = questionary.text("Largura da grade (15):", validate=validar_inteiro_ou_vazio).ask()
    h_str = questionary.text("Altura da grade (15):", validate=validar_inteiro_ou_vazio).ask()
    c_str = questionary.text("Quantidade de coletáveis (3):", validate=validar_inteiro_ou_vazio).ask()
    chance_str = questionary.text("Chance de quebra de parede (0.15):", validate=validar_float_ou_vazio).ask()
    
    w = int(w_str) if w_str != "" else 15
    h = int(h_str) if h_str != "" else 15
    c = int(c_str) if c_str != "" else 3
    chance = float(chance_str) if chance_str != "" else 0.15
    
    print(gerar_labirinto(w, h, c, chance_ciclo=chance))

    input("\nPressione ENTER para continuar...")
    menu_principal()

def menu_principal():
  limpar_terminal()
  choices = {
    "Gerar labirinto": lambda: fluxo_gerador(),
    "Gerar em lote": lambda: menu_gerar_labirintos_lotes(),
    "Resolver o labirinto": lambda: print("Escolheu resolver o labirinto"),
    "Sair": lambda: print("Saindo do programa...")
  }

  escolha = questionary.select("Escolha uma opção:", choices=list(choices.keys())).ask()

  choices.get(escolha, lambda: print("Opção inválida"))()