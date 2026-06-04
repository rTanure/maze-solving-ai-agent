from src.utils.resultados.resultado import Resultado
import pandas as pd

class ResultadoDFS(Resultado):
    def __init__(self):
        super().__init__()
    
    def salvarResultado(self):
        self._salvaResultado(
            "datasets/resultado_dfs.csv",
            {}
        )