import os
import pandas as pd
from src.utils.get_dataframe import get_dataframe
from src.utils.resultados.resultado import Resultado

class ResultadoHillClimbing(Resultado):
    def __init__(self, maze_id):
        super().__init__(maze_id)
        self.curva = []      
        self.iteracoes = 0           
        # --- NOVOS ATRIBUTOS ---
        self.ordem_coletaveis = [] 
        self.rota_macro = []       

    def salvarResultado(self):
        pasta_resultados = "datasets"
        if not os.path.exists(pasta_resultados):
            os.makedirs(pasta_resultados)

        caminho_csv = f"{pasta_resultados}/resultados_hill_climbing.csv"
        df = get_dataframe(caminho_csv)

        novos_dados = {
            "id_labirinto": self.maze_id,
            "sucesso": self.sucesso,
            "custo_final": self.custo,
            "iteracoes": self.iteracoes,
            "ordem_coletaveis": str(self.ordem_coletaveis), # Salvando os coletáveis!
            "rota_macro": str(self.rota_macro),
            "curva_convergencia": str(self.curva)
        }

        df_nova_linha = pd.DataFrame([novos_dados])
        if df.empty:
            df_atualizado = df_nova_linha
        else:
            df_atualizado = pd.concat([df, df_nova_linha], ignore_index=True)

        df_atualizado.to_csv(caminho_csv, index=False)

    @staticmethod
    def get_df():
        return get_dataframe("datasets/resultados_hill_climbing.csv")