from src.utils.gerar_labirintos import gerar_labirinto
from src.utils.get_dataframe import get_dataframe
import pandas as pd
import uuid
import os

class Maze:
    # Se o ID e o maze não forem passados, ele criará um novo labirinto com as informações restantes.
    def __init__(self, width, length, collectibles, cicles, maze = None, id = None):
        self.id = id if id else uuid.uuid4()
        self.maze = maze if maze else gerar_labirinto(width, length, collectibles, cicles)
        self.width = width
        self.length = length
        self.collectibles = collectibles
        self.cicles = cicles

    def save(self):
        caminho_csv = "datasets/mazes.csv"
        df = get_dataframe(caminho_csv)

        if not df.empty and "id" in df.columns and self.id is not None:
            if self.id in df["id"].values:
                print(f"Erro: Já existe um labirinto cadastrado com o ID '{self.id}'.")
                return False

        # --- NOVA PARTE: SALVAR O TXT INDIVIDUAL ---
        pasta_mazes = "datasets/mazes"
        # Garante que a pasta existe
        if not os.path.exists(pasta_mazes):
            os.makedirs(pasta_mazes)
        
        # Define o caminho do arquivo txt usando o ID do labirinto
        caminho_txt = f"{pasta_mazes}/{self.id}.txt"
        
        # Escreve a string do labirinto no arquivo
        with open(caminho_txt, "w", encoding="utf-8") as arquivo_txt:
            arquivo_txt.write(str(self.maze))
        # ------------------------------------------

        novos_dados = {
            "id": self.id,
            "width": self.width,
            "length": self.length,
            "collectibles": self.collectibles,
            "cicles": self.cicles,
        }

        df_nova_linha = pd.DataFrame([novos_dados])
        df_atualizado = pd.concat([df, df_nova_linha], ignore_index=True)
        df_atualizado.to_csv(caminho_csv, index=False)
        
        print(f"Labirinto '{self.id}' salvo no CSV e em '{caminho_txt}' com sucesso!")
        return True

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
            try:
                # Converte a string do labirinto (ex: "[[0, 1], [1, 0]]") de volta para uma lista Python
                maze_estrutura = ast.literal_eval(conteudo_txt)
            except (ValueError, SyntaxError):
                # Caso falhe (ex: se o txt contiver texto puro em vez de formato de lista), mantém como string
                maze_estrutura = conteudo_txt

        # 4. Instancia e retorna o objeto Maze reconstruído
        print(f"Labirinto '{id}' carregado com sucesso!")
        return cls(
            width=int(dados["width"]),
            length=int(dados["length"]),
            collectibles=int(dados["collectibles"]),
            cicles=float(dados["cicles"]),
            maze=maze_estrutura,
            id=str(dados["id"])
        )





