from src.menus.menu_principal import menu_principal
from src.utils.Maze import Maze
from src.utils.buscas.local.hill_climbing_iteracoes import rodar_bateria_hill_climbing
from src.utils.buscas.local.simulated_annealing_iteracoes import rodar_bateria_simulated_annealing

maze = Maze.open('6547fc4a-1594-4807-a504-48d8c6555dc9')
res = rodar_bateria_simulated_annealing(maze, 100, 1000, 0.7)