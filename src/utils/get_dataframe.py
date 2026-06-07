import os
import pandas as pd

def get_dataframe(caminho_arquivo):
    """
    Retorna um DataFrame se o arquivo existir.
    Caso contrário, retorna uma instância de DataFrame vazia sem criar o arquivo fisicamente.
    """
    if os.path.exists(caminho_arquivo):
        # Verifica a extensão para ler corretamente
        if caminho_arquivo.endswith('.xlsx') or caminho_arquivo.endswith('.xls'):
            return pd.read_excel(caminho_arquivo)
        else:
            return pd.read_csv(caminho_arquivo)
    else:
        # Apenas retorna a instância na memória
        return pd.DataFrame()