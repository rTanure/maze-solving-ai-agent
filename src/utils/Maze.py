from src.utils.get_dataframe import get_dataframe
import pandas as pd
import uuid
import os
import numpy as np
import random

class Maze:
    # Se o ID e o maze não forem passados, ele criará um novo labirinto com as informações restantes.
    def __init__(self, width, length, collectibles, cicles, maze, start, end, id = None):
        self.id = id if id else uuid.uuid4()
        if isinstance(maze, str):
            self.maze = [list(linha) for linha in maze.split("\n") if linha]
        else:
            self.maze = maze
        self.width = width
        self.length = length
        self.collectibles = collectibles
        self.cicles = cicles
        self.start = start
        self.end = end

    @classmethod
    def save_all(cls, mazes: list['Maze']) -> bool:
        
        if not mazes:
            print("Nenhum labirinto fornecido para salvar.")
            return False

        caminho_csv = "datasets/mazes.csv"
        df = get_dataframe(caminho_csv)
        
        # Coleta IDs existentes para validação ágil
        ids_existentes = set(df["id"].astype(str).values) if not df.empty and "id" in df.columns else set()
        
        novas_linhas = []
        pasta_mazes = "datasets/mazes"
        
        # Garante que a pasta para os arquivos .txt existe
        if not os.path.exists(pasta_mazes):
            os.makedirs(pasta_mazes)

        # Processa cada labirinto da lista
        for maze in mazes:
            id_str = str(maze.id)
            
            # Validação de ID duplicado (no CSV ou no próprio lote atual)
            if id_str in ids_existentes:
                print(f"Erro pulado: Já existe um labirinto cadastrado com o ID '{id_str}'.")
                continue
            
            # Salva o arquivo .txt individual do labirinto
            caminho_txt = f"{pasta_mazes}/{id_str}.txt"
            with open(caminho_txt, "w", encoding="utf-8") as arquivo_txt:
                if isinstance(maze.maze, list):
                    string_labirinto = "\n".join(["".join(linha) for linha in maze.maze])
                else:
                    string_labirinto = str(maze.maze)
                arquivo_txt.write(string_labirinto)
                
            # Adiciona os metadados na lista de preparação do lote
            novas_linhas.append({
                "id": maze.id,
                "width": maze.width,
                "length": maze.length,
                "collectibles": maze.collectibles,
                "cicles": maze.cicles,
                "start": str(maze.start),  # Salva como string "(x, y)"
                "end": str(maze.end),      # Salva como string "(x, y)"
            })
            
            # Registra o ID para evitar duplicados dentro do próprio lote enviado
            ids_existentes.add(id_str)

        # Se todos os IDs eram repetidos, encerra sem alterar o CSV
        if not novas_linhas:
            print("Nenhum labirinto novo foi salvo.")
            return False

        # Concatena todas as novas linhas e salva o arquivo CSV de uma vez só
        df_novas_linhas = pd.DataFrame(novas_linhas)
        df_atualizado = pd.concat([df, df_novas_linhas], ignore_index=True)
        df_atualizado.to_csv(caminho_csv, index=False)
        
        print(f"Sucesso: {len(novas_linhas)} labirintos foram salvos em lote!")
        return True
    
    @classmethod
    def create(cls, width, height, collectibles=0, cicles=0.1):
        width = int(width)
        height = int(height)
        collectibles = int(collectibles)
        cicles = float(str(cicles).replace(',', '.'))


        if width % 2 == 0: width += 1
        if height % 2 == 0: height += 1


        maze = np.ones((height, width), dtype=int)

        def get_vizinhos(x, y):
            vizinhos = []
            for dx, dy in [(0, 2), (0, -2), (2, 0), (-2, 0)]:
                nx, ny = x + dx, y + dy
                if 0 < nx < width - 1 and 0 < ny < height - 1:
                    vizinhos.append((nx, ny))
            return vizinhos

        stack = [(1, 1)]
        maze[1, 1] = 0
        
        while stack:
            x, y = stack[-1]
            vizinhos = [v for v in get_vizinhos(x, y) if maze[v[1], v[0]] == 1]
            
            if vizinhos:
                nx, ny = random.choice(vizinhos)
                maze[y + (ny - y) // 2, x + (nx - x) // 2] = 0
                maze[ny, nx] = 0
                stack.append((nx, ny))
            else:
                stack.pop()

        for y in range(1, height - 1):
            for x in range(1, width - 1):
                if maze[y, x] == 1:
                    caminho_horizontal = maze[y, x-1] == 0 and maze[y, x+1] == 0 and maze[y-1, x] == 1 and maze[y+1, x] == 1
                    caminho_vertical = maze[y-1, x] == 0 and maze[y+1, x] == 0 and maze[y, x-1] == 1 and maze[y, x+1] == 1
                    
                    if (caminho_horizontal or caminho_vertical) and random.random() < cicles:
                        maze[y, x] = 0

        inicio_x, inicio_y = 1, 1
        fim_x, fim_y = width - 2, height - 2
        
        maze[fim_y, fim_x] = 0
        if maze[fim_y - 1, fim_x] == 1 and maze[fim_y, fim_x - 1] == 1:
            maze[fim_y - 1, fim_x] = 0

        caminhos_livres = list(zip(*np.where(maze == 0)))
        caminhos_livres = [(y, x) for y, x in caminhos_livres if (x, y) != (inicio_x, inicio_y) and (x, y) != (fim_x, fim_y)]
        
        coletaveis_pos = random.sample(caminhos_livres, min(collectibles, len(caminhos_livres)))
        
        matriz_final = np.full((height, width), '#', dtype=str)
        matriz_final[maze == 0] = ' '
        matriz_final[inicio_y, inicio_x] = 'A'
        matriz_final[fim_y, fim_x] = 'B'
        
        for i, (y, x) in enumerate(coletaveis_pos):
            matriz_final[y, x] = 'C'
            
        return Maze(
            start = (inicio_x, inicio_y),
            end = (fim_x, fim_y),
            cicles=cicles,
            collectibles=collectibles,
            length=height,
            width=width,
            maze=matriz_final.tolist()
        )

    @classmethod
    def open(cls, id: str):
        import ast  # Utilizado para converter a string do txt de volta para lista/matriz
        
        caminho_csv = "datasets/mazes.csv"
        caminho_txt = f"datasets/mazes/{id}.txt"
        
        # 1. Verifica se os arquivos necessários existem
        if not os.path.exists(caminho_csv) or not os.path.exists(caminho_txt):
            print(f"Erro: Labirinto com ID '{id}' não foi encontrado nos registros.")
            return None
            
        # 2. Carrega o CSV e busca a linha correspondente ao ID
        df = get_dataframe(caminho_csv)
        if df.empty or "id" not in df.columns:
            print("Erro: O banco de dados de labirintos está vazio ou corrompido.")
            return None
            
        # Filtra a linha que possui o ID desejado
        linha = df[df["id"].astype(str) == str(id)]
        if linha.empty:
            print(f"Erro: ID '{id}' não encontrado no CSV.")
            return None
            
        # Extrai os metadados da primeira linha encontrada
        dados = linha.iloc[0]
        
        # 3. Lê a estrutura do labirinto a partir do arquivo .txt
        with open(caminho_txt, "r", encoding="utf-8") as arquivo_txt:
            conteudo_txt = arquivo_txt.read()
            # Converte as linhas de string de volta para uma lista de listas (vetor)
            maze_vetor = [list(linha) for list_linha in conteudo_txt.split("\n") if (linha := list_linha.strip())]

        # 4. Instancia e retorna o objeto Maze reconstruído
        start_tuple = ast.literal_eval(str(dados["start"])) if "start" in dados else (1, 1)
        end_tuple = ast.literal_eval(str(dados["end"])) if "end" in dados else (int(dados["width"])-2, int(dados["length"])-2)

        return cls(
            width=int(dados["width"]),
            length=int(dados["length"]),
            collectibles=int(dados["collectibles"]),
            cicles=float(dados["cicles"]),
            maze=maze_vetor,
            id=str(dados["id"]),
            start=start_tuple,
            end=end_tuple,
        )
    
    @classmethod
    def get_ids(cls) -> list[str]:
        caminho_csv = "datasets/mazes.csv"
            
        df = get_dataframe(caminho_csv)
        
        if df.empty or "id" not in df.columns:
            return []
            
        # Converte os IDs para string e retorna como uma lista nativa do Python
        return df["id"].astype(str).tolist()





