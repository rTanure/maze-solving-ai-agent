from src.menus.menu_principal import menu_principal
from src.utils.Maze import Maze
from src.utils.buscas.classicas.dfs import dfs
from src.utils.buscas.gerencia_busca import GerenciadorDeBusca

maze = Maze.open("329de47a-d4ad-41d9-8e1d-3fd0454068e4")

buscas = GerenciadorDeBusca()

res = buscas.executar_busca("DFS", maze)

print(res[1])