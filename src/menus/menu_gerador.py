import questionary
from src.utils.validadores import *
from src.utils.Maze import Maze
import random

def menu_gerar_labirintos_lotes():
    valida_int = lambda x: True if (x == "" or (x.isdigit() and int(x) >= 0)) else "Digite um número inteiro maior ou igual a 0"
    valida_float_0_1 = lambda x: True if (x == "" or (x.replace(',', '.').replace('.', '', 1).isdigit() and 0.0 <= float(x.replace(',', '.')) <= 1.0)) else "Digite um valor decimal entre 0.0 e 1.0"
    valida_max_width = lambda x: True if (x == "" or int(x) >= int(min_width)) else f"A largura máxima deve ser maior ou igual à mínima ({min_width})"
    valida_max_length = lambda x: True if (x == "" or int(x) >= int(min_length)) else f"O comprimento máximo deve ser maior ou igual ao mínimo ({min_length})"
    valida_max_collect = lambda x: True if (x == "" or int(x) >= int(min_collectibles)) else f"O máximo de coletáveis deve ser maior ou igual ao mínimo ({min_collectibles})"
    valida_max_cicle = lambda x: True if (x == "" or float(x.replace(',', '.')) >= float(min_cicle.replace(',', '.'))) else f"O ciclo máximo deve ser maior ou igual ao mínimo ({min_cicle})"

    min_width = questionary.text("Largura mínima (padrão 5):", validate=valida_int).ask()
    max_width = questionary.text(f"Largura máxima (padrão 1000):", validate=lambda x: valida_int(x) if valida_int(x) != True else valida_max_width(x)).ask()
    min_length = questionary.text("Comprimento mínimo (padrão 5):", validate=valida_int).ask()
    max_length = questionary.text("Comprimento máximo (padrão 1000):", validate=lambda x: valida_int(x) if valida_int(x) != True else valida_max_length(x)).ask()
    min_collectibles = questionary.text("Coletáveis mínimo (padrão 0)", validate=valida_int).ask()
    max_collectibles = questionary.text("Coletáveis máximo (padrão 26):", validate=lambda x: valida_int(x) if valida_int(x) != True else valida_max_collect(x)).ask()
    min_cicle = questionary.text("Probabilidade de ciclo mínimo (padrão 0.1):", validate=valida_float_0_1).ask()
    max_cicle = questionary.text("Probabilidade de ciclo máximo (padrão 0.2):", validate=lambda x: valida_float_0_1(x) if valida_float_0_1(x) != True else valida_max_cicle(x)).ask()
    number_of_mazes = questionary.text("Quantidade de labirintos (padrão 15):", validate=valida_int).ask()

    min_width = int(min_width) if min_width else 5
    max_width = int(max_width) if max_width else 1000
    min_length = int(min_length) if min_length else 5
    max_length = int(max_length) if max_length else 1000
    min_collectibles = int(min_collectibles) if min_collectibles else 0
    max_collectibles = int(max_collectibles) if max_collectibles else 26
    if min_collectibles > max_collectibles:
        min_collectibles, max_collectibles = max_collectibles, min_collectibles

    min_cicle = float(min_cicle.replace(',', '.')) if min_cicle else 0.1
    max_cicle = float(max_cicle.replace(',', '.')) if max_cicle else 0.2
    
    number_of_mazes = int(number_of_mazes) if number_of_mazes else 15

    print(f"\nGerando {number_of_mazes} labirintos...")
    for _ in range(number_of_mazes):
        width = random.randint(min_width, max_width)
        length = random.randint(min_length, max_length)
        collectibles = random.randint(min_collectibles, max_collectibles)
        cicles = random.uniform(min_cicle, max_cicle)

        maze = Maze(width, length, collectibles, cicles)
        maze.save()