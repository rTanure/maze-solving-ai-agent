from src.utils.run_missing_results import run_missing_results
from src.utils.buscas.local.hill_climbing_iteracoes import rodar_bateria_hill_climbing
from src.utils.buscas.local.simulated_annealing_iteracoes import rodar_bateria_simulated_annealing
from src.utils.Maze import Maze

maze = Maze.open("65689af1-9540-4fd1-ba62-740863d78865")

rodar_bateria_simulated_annealing(maze)