import os
import pandas as pd
from tabula.io import read_pdf
import re

# Diretório contendo os arquivos PDF
diretorio_pdf = r'C:\Users\ronal\OneDrive\Auto-GPT\Auto-GPT-0.4.7\auto_gpt_workspace\recupera'

# Lista de arquivos PDF no diretório
arquivos_pdf = [os.path.join(diretorio_pdf, arquivo) for arquivo in os.listdir(diretorio_pdf) if arquivo.endswith('.pdf')]

# Loop através dos arquivos PDF e consultar os dados
for arquivo_pdf in arquivos_pdf:
    print(f"Consultando dados de {arquivo_pdf}:")

    # Use a função read_pdf para ler o PDF e extrair tabelas (pode haver várias)
    tabelas = read_pdf(arquivo_pdf, pages='all')

    # Verifique se há pelo menos uma tabela extraída
    if tabelas:
        # A primeira tabela é tabelas[0]
        primeira_tabela = tabelas[12]  # Suponha que a tabela desejada seja a tabela 13

        # Verifique se alguma coluna contém a string "Receita Bruta Informada"
        colunas_com_valor = primeira_tabela.columns.str.contains("Receita Bruta Informada")

        # Verifique se alguma coluna contém a string
        if colunas_com_valor.any():
            coluna = primeira_tabela.columns[colunas_com_valor][0]
            valor = primeira_tabela.loc[3, coluna]

            # Aplicar a expressão regular para extrair valores numéricos ou de moeda
            padrao_numerico = r'(?<!Parcela\s)(\d{1,3}(?:[.,]\d{3})*(?:[.,]\d{2}))(?!\d)'
            correspondencias = re.findall(padrao_numerico, valor)

            if correspondencias:
                # Concatenar todas as correspondências para formar o valor final
                valor = ''.join(correspondencias)
                # Remover pontos (.) de milhares
                valor = valor.replace('.', '')
                # Substituir vírgulas (,) por pontos (.) como separadores decimais
                valor = valor.replace(',', '.')
                # Converter para ponto flutuante
                valor = float(valor)
                print(f"Valor numérico: {valor}")
            else:
                print("Nenhum valor numérico encontrado.")
        else:
            print("A coluna 'Receita Bruta Informada' não existe na tabela.")
    else:
        print("Nenhuma tabela encontrada neste arquivo.")
