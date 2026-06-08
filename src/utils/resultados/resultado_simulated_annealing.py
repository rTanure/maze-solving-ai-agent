import os
import pandas as pd
from src.utils.get_dataframe import get_dataframe
from src.utils.resultados.resultado import Resultado

class ResultadoSimulatedAnnealing(Resultado):
    def __init__(self, maze_id):
        super().__init__(maze_id)
        self.curva = []      
        self.iteracoes = 0     
        
        # --- NOVOS ATRIBUTOS ---
        self.ordem_coletaveis = [] 
        self.rota_macro = [] 

        self.pior_custo = None
        self.custo_medio = None
        self.tempo_medio = None
        self.iteracoes_media = None
        self.taxa_sucesso = None       

    def salvarResultado(self):
        self._salvaResultado(
            "datasets/resultados_simulated_annealing.csv",
            {
                "iteracoes": str(self.iteracoes),
                "ordem_coletaveis": str(self.ordem_coletaveis), # Salvando os coletáveis!
                "rota_macro": str(self.rota_macro),
                "curva_convergencia": str(self.curva),
                "pior_custo": str(self.pior_custo) if self.pior_custo is not None else "",
                "custo_medio": f"{self.custo_medio:.2f}" if self.custo_medio is not None else "",
                "tempo_medio": f"{self.tempo_medio:.6f}" if self.tempo_medio is not None else "",
                "iteracoes_media": f"{self.iteracoes_media:.2f}" if self.iteracoes_media is not None else "",
                "taxa_sucesso_5porcento": f"{self.taxa_sucesso:.1f}%" if self.taxa_sucesso is not None else ""
                
            }   
        )

    @staticmethod
    def get_df():
        return get_dataframe("datasets/resultados_simulated_annealing.csv")
