import os
import pandas as pd
from src.utils.get_dataframe import get_dataframe
from src.utils.resultados.resultado import Resultado

class ResultadoHillClimbing(Resultado):
    def __init__(self, maze_id):
        super().__init__(maze_id)
        self.curva = []      
        self.iteracoes = 0           
        self.ordem_coletaveis = [] 
        self.rota_macro = []

        self.minimo_local = False       

    def salvarResultado(self):
        self._salvaResultado(
            "datasets/resultados_hill_climbing.csv",
            {
                "iteracoes": str(self.iteracoes),
                "ordem_coletaveis": str(self.ordem_coletaveis), # Salvando os coletáveis!
                "rota_macro": str(self.rota_macro),
                "curva_convergencia": str(self.curva)
            }
        )

    @staticmethod
    def get_df():
        return get_dataframe("datasets/resultados_hill_climbing.csv")