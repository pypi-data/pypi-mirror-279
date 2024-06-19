import pandas as pd
import requests
import pyreadstat
import tempfile
import os
from tabulate import tabulate

def download_and_load_sav_file(public_url):

    """
    Baixa um arquivo .sav do OneDrive e carrega os dados em um DataFrame.

    Args:
    public_url (str): URL pública direta do arquivo no OneDrive com o parâmetro de download.

    Returns:
    DataFrame: DataFrame carregado a partir do arquivo .sav ou None se houver um erro.
    """
    # Criar um diretório temporário
    with tempfile.TemporaryDirectory() as tmpdirname:
        # Nome do arquivo
        file_name = 'downloaded_file.sav'
        downloaded_file_path = os.path.join(tmpdirname, file_name)

        try:
            # Baixar o arquivo do OneDrive
            response = requests.get(public_url)
            response.raise_for_status()  # Levanta um erro para códigos de status de resposta ruins

            # Salvar o arquivo no diretório temporário
            with open(downloaded_file_path, 'wb') as file:
                file.write(response.content)
            print("Arquivo baixado com sucesso.")

            # Carregar o DataFrame
            df, meta = pyreadstat.read_sav(downloaded_file_path)
            print("DataFrame carregado com sucesso.")
            return df, meta

        except requests.RequestException as req_err:
            print("Erro ao baixar o arquivo:", req_err)
        except pyreadstat.ReadstatError as read_err:
            print("Erro ao carregar o arquivo:", read_err)
        except Exception as e:
            print("Erro inesperado:", e)

    return None

def generate_frequency_table(df, meta, coluna):

    """
    Gera uma tabela de frequência para uma coluna específica de um DataFrame.

    Parâmetros:
    df (pandas.DataFrame): DataFrame contendo os dados.
    meta (pyreadstat.Meta): Metadados do arquivo SAV.
    coluna (str): Nome da coluna para a qual a tabela de frequência será gerada.

    Exibe:
    Tabela de frequência com os valores, frequências, percentuais e percentuais cumulativos.
    """
    # Mapear os valores para labels usando meta.variable_value_labels
    value_labels = meta.variable_value_labels.get(coluna, {})

    # Criar a tabela de frequência
    frequency_table = df[coluna].value_counts(dropna=False).sort_index().reset_index()
    frequency_table.columns = [coluna, 'Frequency']
    frequency_table['Value Labels'] = frequency_table[coluna].map(value_labels)

    # Reordenar as colunas
    frequency_table = frequency_table[[coluna, 'Value Labels', 'Frequency']]

    # Calcular os percentuais
    total_cases = len(df)
    frequency_table['Percent'] = (frequency_table['Frequency'] / total_cases * 100).round(2)
    frequency_table['Cumulative Percent'] = frequency_table['Percent'].cumsum().round(2)

    # Adicionar linha de Total
    total_row = pd.DataFrame({
        coluna: ['Total'], 
        'Value Labels': [''], 
        'Frequency': [frequency_table['Frequency'].sum()], 
        'Percent': [''], 
        'Cumulative Percent': ['']
    })
    frequency_table = pd.concat([frequency_table, total_row], ignore_index=True)

    # Exibir a tabela
    print(tabulate(frequency_table, headers='keys', tablefmt='grid', showindex=False))