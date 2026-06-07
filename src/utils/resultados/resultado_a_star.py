from src.utils.resultados.resultado import Resultado
from src.utils.get_dataframe import get_dataframe
import pandas as pd

class ResultadoAStar(Resultado):
    def __init__(self, maze_id):
        super().__init__(maze_id)

    def salvarResultado(self):
        self._salvaResultado(
            "datasets/resultado_a_star.csv",
            {}
        )
    
    @staticmethod
    def get_df():
        return get_dataframe("datasets/resultado_a_star.csv")
