from src.utils.resultados.resultado import Resultado
from src.utils.get_dataframe import get_dataframe

class ResultadoOnlineAStar(Resultado):
    def __init__(self, maze_id):
        super().__init__(maze_id)
        self.celulas_reveladas = 0
        self.celulas_revisitadas = 0
        self.replanejamentos = 0
        self.custo_real = 0
        self.grid_interno
        
    def _getResultado(self):
        base = super()._getResultado()
        
        base.update({
            "celulas_reveladas": [self.celulas_reveladas],
            "celulas_revisitadas": [self.celulas_revisitadas],
            "replanejamentos": [self.replanejamentos],
            "custo_real": [self.custo_real]
        })
        return base

    def salvarResultado(self):
        self._salvaResultado(
            "datasets/resultado_online_a_star.csv",
            {}
        )
        
    @staticmethod
    def get_df():
        return get_dataframe("datasets/resultado_online_a_star.csv")