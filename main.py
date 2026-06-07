from src.menus.menu_principal import menu_principal
from src.utils.gerar_labirintos import gerar_labirinto
from src.utils.Maze import Maze
from src.utils.buscas.classicas.dfs import dfs

maze = Maze.open("329de47a-d4ad-41d9-8e1d-3fd0454068e4")

print(dfs(maze.maze))

