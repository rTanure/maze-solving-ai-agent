from src.utils.resultados.resultado import Resultado
import pandas as pd
import os

class ResultadoOnlineAStar(Resultado):
    def __init__(self):
        super().__init__()
        self.celulas_reveladas = 0
        self.celulas_revisitadas = 0
        self.replanejamentos = 0
        
    def _getResultado(self):
        base = super()._getResultado()
        base.update({
            "celulas_reveladas": [self.celulas_reveladas],
            "celulas_revisitadas": [self.celulas_revisitadas],
            "replanejamentos": [self.replanejamentos]
        })
        return base

    def salvarResultado(self):
        self._salvaResultado(
            "datasets/resultado_online_astar.csv",
            {}
        )