import os
import pandas as pd
from tabula.io import read_pdf
import re
from PyPDF2 import PdfReader

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
    if isinstance(celula, str) and "Revenda de mercadorias, exceto para o exterior" in celula:
        return coluna
    return None

# Expressão regular para procurar a string
expressao = "CNPJ Estabelecimento:"

# Função para verificar se a expressão está presente em uma tabela
def verifica_tabela(tabela):
    for coluna in tabela.columns:
        for valor in tabela[coluna]:
            if isinstance(valor, str) and expressao in valor:
                return True
    return False

# Inicialize a variável para armazenar a soma
soma_valores = 0

# Inicialize a variável para contar a quantidade de expressões encontradas
quantidade_expressoes = 0

# Loop através dos arquivos PDF e consultar os dados
for arquivo_pdf in arquivos_pdf:
    print(f"Consultando dados de {arquivo_pdf}:")

    # Use a função read_pdf para ler o PDF e extrair tabelas (pode haver várias)
    tabelas = read_pdf(arquivo_pdf, pages='all')

    # Verifique se há pelo menos uma tabela extraída
    if tabelas:
        encontrou = False
        for idx, tabela in enumerate(tabelas):
            print(f"Tabela {idx + 1}:")

             # Verifique se a expressão está presente na tabela atual
            if tabela.columns.str.contains(expressao).any():
                encontrou = True
                print(f"A expressão '{expressao}' foi encontrada na Tabela {idx + 1} do arquivo.")
                quantidade_expressoes += 1  # Incrementar a contagem de expressões encontradas

            # Verifique se alguma coluna contém a string "Revenda de mercadorias, exceto para o exterior"
            colunas_com_valor = tabela.columns.str.contains("Revenda de mercadorias, exceto para o exterior") | tabela.applymap(lambda celula: verifica_celula(celula, tabela.columns.any())).any().to_numpy()

            #colunas_com_valor_celula = tabela.applymap(lambda celula: verifica_celula(celula, tabela.columns.any())).any().to_numpy()
            
            # Verifique se alguma coluna contém a string
            if colunas_com_valor.any():
                coluna = tabela.columns[colunas_com_valor][0]

                # Inicialize a variável para rastrear o estado
                estado = None

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
                                # Adicionar o valor à soma
                                soma_valores += valor
                        elif "Parcela" in valor:
                            estado = "ativo"  # Ativar o estado quando "Parcela" é encontrado
                    
                    else:
                        print("Apesar de estar na coluna correta, o valor selecionado não é uma string.")
            else:
                print(f"A coluna 'Revenda de mercadorias, exceto para o exterior' não existe na tabela {idx + 1}.")
    else:
        print("Nenhuma tabela encontrada neste arquivo.")

# Imprima a soma dos valores e a quantidade de expressões encontradas ao final do loop
print(f"Soma dos Valores Numéricos: {soma_valores}")
print(f"Quantidade de CNPJ Encontradas: {quantidade_expressoes}")
