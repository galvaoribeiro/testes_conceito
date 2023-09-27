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
        if colunas_com_valor.any(): #Esta linha verifica se a variável colunas_com_valor contém pelo menos um valor verdadeiro. 'colunas_com_valor' é uma série booleana que indica para cada coluna se o nome da coluna contém a string "Receita Bruta Informada" (ou seja, é verdadeiro se a string está presente na coluna). O método any() verifica se pelo menos um valor na série é verdadeiro.
            coluna = primeira_tabela.columns[colunas_com_valor][0] #Se houver pelo menos uma coluna que contenha a string "Receita Bruta Informada", esta linha obtém o nome da primeira coluna que satisfaça essa condição
            valor = primeira_tabela.loc[3, coluna] # Após encontrar a coluna desejada, esta linha obtém o valor na primeira linha (linha 0) dessa coluna. '0' é o número da linha e coluna é o nome da coluna que foi encontrado anteriormente.
            #print(f"Valor: {valor}, Coluna: {coluna}")
            
            print(f"Valor: {valor}")
        else:
            print("A coluna 'Receita Bruta Informada' não existe na tabela.")
    else:
        print("Nenhuma tabela encontrada neste arquivo.")
