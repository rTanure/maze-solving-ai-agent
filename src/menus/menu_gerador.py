import questionary
from src.utils.validadores import *
from src.utils.Maze import Maze
import random

def menu_gerar_labirintos_lotes():
    min_width = questionary.text("Largura mínima (padrão 5):").ask()
    max_width = questionary.text(f"Largura máxima (padrão 100):").ask()
    min_height = questionary.text("Comprimento mínimo (padrão 5):").ask()
    max_height = questionary.text("Comprimento máximo (padrão 100):").ask()
    min_collectibles = questionary.text("Coletáveis mínimo (padrão 0)").ask()
    max_collectibles = questionary.text("Coletáveis máximo (padrão 10):").ask()
    min_cicle = questionary.text("Probabilidade de ciclo mínimo (padrão 0):").ask()
    max_cicle = questionary.text("Probabilidade de ciclo máximo (padrão 0.5):").ask()
    number_of_mazes = questionary.text("Quantidade de labirintos (padrão 10):").ask()

    min_width = int(min_width) if min_width else 5
    max_width = int(max_width) if max_width else 100
    min_height = int(min_height) if min_height else 5
    max_height = int(max_height) if max_height else 100
    if min_width < 5: min_width = 5
    if max_width < 5: max_width = 5
    if min_height < 5: min_height = 5
    if max_height < 5: max_height = 5
    min_collectibles = int(min_collectibles) if min_collectibles else 0
    max_collectibles = int(max_collectibles) if max_collectibles else 10
    if min_collectibles > max_collectibles:
        min_collectibles, max_collectibles = max_collectibles, min_collectibles

    min_cicle = float(min_cicle.replace(',', '.')) if min_cicle else 0
    max_cicle = float(max_cicle.replace(',', '.')) if max_cicle else 0.5
    
    number_of_mazes = int(number_of_mazes) if number_of_mazes else 10
    

    print(f"\nGerando {number_of_mazes} labirintos...")
    mazes = []
    for _ in range(number_of_mazes):
        width = random.randint(min_width, max_width)
        height = random.randint(min_height, max_height)

        collectibles = random.randint(min_collectibles, max_collectibles)
        cicles = random.uniform(min_cicle, max_cicle)

        mazes.append(Maze.create(width, height, collectibles, cicles))
    
    Maze.save_all(mazes)
