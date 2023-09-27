import os
import pandas as pd
from tabula.io import read_pdf

# Diretório contendo os arquivos PDF
diretorio_pdf = r'C:\Users\ronal\OneDrive\Auto-GPT\Auto-GPT-0.4.7\auto_gpt_workspace\recupera'


# Lista de DataFrames para armazenar as tabelas extraídas
tabelas_dataframes = []

# Lista de arquivos PDF no diretório
arquivos_pdf = [os.path.join(diretorio_pdf, arquivo) for arquivo in os.listdir(diretorio_pdf) if arquivo.endswith('.pdf')]

# Loop através dos arquivos PDF e consultar os dados
for arquivo_pdf in arquivos_pdf:
    print(f"Consultando dados de {arquivo_pdf}:")

    # Use a função read_pdf para ler o PDF e extrair tabelas (pode haver várias)
    tabelas = read_pdf(arquivo_pdf, pages='all')

    # Loop através das tabelas extraídas
    for tabela in tabelas:
        # Converta a tabela em um DataFrame do pandas
        df = pd.DataFrame(tabela)

        # Adicione o DataFrame à lista de DataFrames
        tabelas_dataframes.append(df)

# Agora você tem uma lista de DataFrames contendo as tabelas extraídas
# Você pode acessar cada DataFrame da lista como necessário
for idx, dataframe in enumerate(tabelas_dataframes):
    print(f"Tabela {idx + 1}:")
    print(dataframe)
