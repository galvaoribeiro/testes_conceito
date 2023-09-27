


import os
import pandas as pd
from tabula.io import read_pdf
from openpyxl import Workbook
from openpyxl.utils.dataframe import dataframe_to_rows

# Diretório contendo os arquivos PDF
diretorio_pdf = r'C:\Users\ronal\OneDrive\Auto-GPT\Auto-GPT-0.4.7\auto_gpt_workspace\recupera'

# Lista de arquivos PDF no diretório
arquivos_pdf = [os.path.join(diretorio_pdf, arquivo) for arquivo in os.listdir(diretorio_pdf) if arquivo.endswith('.pdf')]

# Crie um arquivo Excel
arquivo_excel = 'dados_extraidos.xlsx'
wb = Workbook()

# Loop através dos arquivos PDF e consultar os dados
for arquivo_pdf in arquivos_pdf:
    print(f"Consultando dados de {arquivo_pdf}:")

    # Use a função read_pdf para ler o PDF e extrair tabelas (pode haver várias)
    tabelas = read_pdf(arquivo_pdf, pages='all')

    # Loop através das tabelas extraídas
    for idx, tabela in enumerate(tabelas):
        # Converta a tabela em um DataFrame do pandas
        df = pd.DataFrame(tabela)

        # Crie uma nova planilha no arquivo Excel
        planilha = wb.create_sheet(title=f'Tabela_{idx + 1}')

        # Use dataframe_to_rows para converter o DataFrame em linhas para o Excel
        for linha in dataframe_to_rows(df, index=False, header=True):
            planilha.append(list(linha))  # Converta a linha do DataFrame em uma lista

# Salve o arquivo Excel
wb.remove(wb['Sheet'])  # Remova a planilha padrão
wb.save(arquivo_excel)
print(f'Dados exportados para {arquivo_excel}')

