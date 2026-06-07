from src.utils.resultados.resultado import Resultado
from src.utils.get_dataframe import get_dataframe
import pandas as pd

class ResultadoGuloso(Resultado):
    def __init__(self, maze_id):
        super().__init__(maze_id)
    
    def salvarResultado(self):
        self._salvaResultado(
            "datasets/resultado_guloso.csv",
            {}
        )
    
    @staticmethod
    def get_df():
        return get_dataframe("datasets/resultado_guloso.csv")