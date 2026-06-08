from abc import ABC, abstractmethod
import time

import pandas as pd
import os

class Resultado(ABC):
    def __init__(self, maze_id):
        self.sucesso = False
        self.maze_id = maze_id if maze_id else print(">>> Id deve ser passado!!!")
        self.custo = 0
        self.passos = 0
        self.expandidos = 0
        self.fronteira = 0
        self.tempo = 0
        self.inicio = 0
        self.fim = 0
        self.caminho = []
    
    def addCusto(self, increment = 1):
        self.custo += increment
    
    def addPassos(self, increment = 1):
        self.passos += increment
    
    def addExpandidos(self, increment = 1):
        self.expandidos += increment
    
    def addfronteira(self, increment = 1):
        self.fronteira += increment

    def start(self):
        self.inicio = time.perf_counter()
    
    def finish(self):
        self.fim = time.perf_counter()
        self.tempo = self.fim - self.inicio
    
    def _getResultado(self): 
        return {
            "maze_id": [self.maze_id],
            "sucesso": [self.sucesso],
            "custo": [self.custo],
            "passos": [self.passos],
            "expandidos": [self.expandidos],
            "fronteira": [self.fronteira],
            "tempo_segundos": [self.tempo],
            "caminho": [self.caminho]
        }

    def _salvaResultado(self, file, additionalData):
        dados = self._getResultado() | additionalData

        df_dados = pd.DataFrame(dados, index=[0])

        pasta = os.path.dirname(file)
        if pasta and not os.path.exists(pasta):
            os.makedirs(pasta, exist_ok=True) 
        # Se o arquivo existe e não está vazio, faz o append correto
        if os.path.exists(file) and os.path.getsize(file) > 0:
            try:
                df_atual = pd.read_csv(file)
                df_concat = pd.concat([df_atual, df_dados], ignore_index=True)
            except Exception:
                # Caso o arquivo esteja corrompido de alguma forma anterior, resguarda os dados novos
                df_concat = df_dados
        else:
            df_concat = df_dados

        # Salva o arquivo finalizado
        df_concat.to_csv(file, index=False)
        

    @abstractmethod
    def salvarResultado():
        pass
    
    @abstractmethod
    def get_df():
        pass
