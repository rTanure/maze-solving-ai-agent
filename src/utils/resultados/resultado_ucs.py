from resultado import Resultado
import pandas as pd
import os

class ResultadoUCS(Resultado):
    def __init__(self):
        super().__init__()
    
    def salvarResultado(self):
        self._salvaResultado(
            "datasets/resultado_ucs.csv",
            {}
        )