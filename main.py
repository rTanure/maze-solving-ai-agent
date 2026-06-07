from src.menus.menu_principal import menu_principal
from src.utils.Maze import Maze
from src.utils.buscas.classicas.dfs import dfs
from src.utils.buscas.gerencia_busca import GerenciadorDeBusca
import random

# menu_principal()

maze = Maze.open("cfd0b46d-77ed-433d-8744-d409f64c4e75")
buscas = GerenciadorDeBusca()
res = buscas.executar_busca("BFS", maze)
print(res.caminho)