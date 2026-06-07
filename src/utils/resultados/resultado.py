from abc import ABC, abstractmethod
import time

import pandas as pd
import os

class Resultado(ABC):
    def __init__(self):
        self.sucesso = False
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
            "sucesso": [self.sucesso],
            "custo": [self.custo],
            "passos": [self.passos],
            "expandidos": [self.expandidos],
            "fronteira": [self.fronteira],
            "tempo_segundos": [self.tempo],
        }

    def _salvaResultado(self, file, additionalData):
        dados = self._getResultado() | additionalData

        df_dados = pd.DataFrame(dados, index=[0])

        pasta = os.path.dirname(file)
        if pasta and not os.path.exists(pasta):
            os.makedirs(pasta)

        if os.path.exists(file):
            df_atual = pd.read_csv(file)
            df_concat = pd.concat([df_atual, df_dados], ignore_index=True)
        else:
            df_concat = df_dados

        df_concat.to_csv(file, index=False)
        

    @abstractmethod
    def salvarResultado():
        pass
