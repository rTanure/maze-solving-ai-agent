import os
import pandas as pd

def get_dataframe(caminho_arquivo):
    """
    Retorna um DataFrame se o arquivo existir.
    Caso contrário, cria um arquivo CSV vazio com o nome fornecido e retorna um DataFrame vazio.
    """
    if os.path.exists(caminho_arquivo):
        # Verifica a extensão para ler corretamente (suporta CSV ou Excel básico)
        if caminho_arquivo.endswith('.xlsx') or caminho_arquivo.endswith('.xls'):
            return pd.read_excel(caminho_arquivo)
        else:
            return pd.read_csv(caminho_arquivo)
    else:
        print(f"Arquivo não encontrado. Criando um novo CSV em: '{caminho_arquivo}'...")
        
        # Cria um DataFrame vazio
        df_vazio = pd.DataFrame()
        
        # Garante que as pastas do caminho existam antes de salvar
        diretorio = os.path.dirname(caminho_arquivo)
        if diretorio and not os.path.exists(diretorio):
            os.makedirs(diretorio)
            
        # Salva o arquivo CSV vazio (index=False evita colunas sem nome)
        df_vazio.to_csv(caminho_arquivo, index=False)
        return df_vazio