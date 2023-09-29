import os
import pandas as pd
from tabula.io import read_pdf
import re
import numpy as np

# Diretório contendo os arquivos PDF
diretorio_pdf = r'C:\Users\ronal\OneDrive\Auto-GPT\Auto-GPT-0.4.7\auto_gpt_workspace\recupera'

# Lista de arquivos PDF no diretório
arquivos_pdf = [os.path.join(diretorio_pdf, arquivo) for arquivo in os.listdir(diretorio_pdf) if arquivo.endswith('.pdf')]

# Expressão regular para extrair valores numéricos ou de moeda
padrao_numerico = r'(?<!Parcela\s)(\d{1,3}(?:[.,]\d{3})*(?:[.,]\d{2}))(?!\d)'

# Função para verificar se uma linha contém a expressão desejada
def verifica_linha(linha):
    return "Tributação monofásica de: COFINS, PIS" in linha


# Função para verificar se uma célula contém a expressão desejada
def verifica_celula(celula, coluna):
    if isinstance(celula, str) and "Receita Bruta Informada" in celula:
        return coluna
    return None


# Loop através dos arquivos PDF e consultar os dados
for arquivo_pdf in arquivos_pdf:
    print(f"Consultando dados de {arquivo_pdf}:")

    # Use a função read_pdf para ler o PDF e extrair tabelas (pode haver várias)
    tabelas = read_pdf(arquivo_pdf, pages='all')

    # Verifique se há pelo menos uma tabela extraída
    if tabelas:
        for idx, tabela in enumerate(tabelas):
            print(f"Tabela {idx + 1}:")
            
            # Verifique se alguma coluna contém a string "Receita Bruta Informada"
            colunas_com_valor = tabela.columns.str.contains("Receita Bruta Informada") | tabela.applymap(lambda celula: verifica_celula(celula, tabela.columns.any())).any().to_numpy()

            colunas_com_valor_celula = tabela.applymap(lambda celula: verifica_celula(celula, tabela.columns.any())).any().to_numpy()
            
            # Verifique se alguma coluna contém a string
            if colunas_com_valor.any():
                coluna = tabela.columns[colunas_com_valor][0]

                # Inicialize a variável para rastrear o estado
                estado = None
                valores = []  # Inicialize uma lista para armazenar os valores

                for valor in tabela[coluna]:
                    if isinstance(valor, str):
                        if estado == "ativo":
                            # Aplicar a expressão regular para extrair valores numéricos ou de moeda
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
                        elif "Parcela" in valor:
                            estado = "ativo"  # Ativar o estado quando "Parcela" é encontrado
                    else:
                        print("O valor não é uma string.")
            else:
                print("A coluna 'Receita Bruta Informada' não existe na tabela.")
    else:
        print("Nenhuma tabela encontrada neste arquivo.")
