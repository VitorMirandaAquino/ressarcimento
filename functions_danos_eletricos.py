from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import UnexpectedAlertPresentException

import time

import pandas as pd
import numpy as np
import re
import streamlit as st

import requests
import os


def download_imagem_dentro_loop(navegador, xpath, caminho, nome_arquivo):
    
    time.sleep(3)

    # Aguarde até que o botão seja clicável
    botao = WebDriverWait(navegador, 15).until(EC.element_to_be_clickable((By.XPATH, xpath)))
    
    # Clique no botão para baixar a imagem
    botao.click()

    # Alterar o navegador para a aba de download de documentos
    WebDriverWait(navegador, 10).until(
        EC.number_of_windows_to_be(3))
    
    time.sleep(1)
    
    # Obtenha uma lista de identificadores de janelas
    janelas_abertas = navegador.window_handles

    # Determine o número de janelas abertas
    numero_janelas = len(janelas_abertas)

    if numero_janelas > 2:

        new_window_handle = navegador.window_handles[2]
        navegador.switch_to.window(new_window_handle)

        # Obtenha a URL da imagem
        url_imagem = navegador.current_url

        time.sleep(5)

        navegador.close()

        # Volte para a janela anterior
        navegador.switch_to.window(navegador.window_handles[1])

        # Baixe a imagem usando requests
        response = requests.get(url_imagem)

        # Verifique se a solicitação foi bem-sucedida (código de status 200)
        if response.status_code == 200:

            # Verifique se o diretório de salvamento existe, se não, crie
            if not os.path.exists(caminho):
                os.makedirs(caminho)
            
            # Salve a imagem localmente no diretório especificado
            with open(os.path.join(caminho, f"{nome_arquivo}.jpg"), "wb") as file:
                file.write(response.content)
        else:
            print("Não foi possível baixar a imagem.")


    return navegador

def processar_texto(texto, lista_documentos):
    """
    Processa o texto para encontrar o número de arquivos adicionados para cada documento na lista de documentos.
    
    Args:
    texto (str): O texto a ser processado.
    lista_documentos (list): Lista de documentos a serem procurados no texto.

    Returns:
    dict: Um dicionário com a contagem de arquivos e as partes do texto para cada documento.
    """

    # Quebrar o texto em partes após "arquivo adicionado"
    partes_texto = re.split(r'arquivo[s]? adicionado[s]?', texto)

    # Dicionário para armazenar a contagem de documentos e o número de arquivos
    info_documentos = {doc: {'arquivos': 0, 'partes': np.nan} for doc in lista_documentos}

    # Esperar um tempo (se necessário)
    time.sleep(5)

    # Iterar sobre as partes do texto
    for i, parte in enumerate(partes_texto):
        # Adicionando "arquivos" no final do trecho
        parte = parte + "arquivos"
        parte_index = i + 1
        
        # Iterar sobre os documentos
        for documento in lista_documentos:
            # Verificar se o documento está presente na parte
            if documento in parte:
                # Procurar pelo número de arquivos
                correspondencia_arquivos = re.search(r'(\d+) arquivos', parte)
                if correspondencia_arquivos:
                    # Atualizar as informações do documento
                    quantidade_arquivos = int(correspondencia_arquivos.group(1))
                    info_documentos[documento]['arquivos'] = quantidade_arquivos
                    info_documentos[documento]['partes'] = parte_index

    return info_documentos


def processar_linha(navegador, row, path_generico_multiplo, path_generico_individual, caminho, num_processo, scroll_length):
    # Converte row['partes'] para inteiro antes de usar na operação matemática
    partes_int = int(row['partes'])

    # Rola a página para baixo para garantir que o botão seja visível
    navegador.execute_script(f"window.scrollTo(0, {str(scroll_length + partes_int * 200)});")
    # navegador.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    time.sleep(2)

    nome_documento = row.name
    nome_documento = nome_documento.replace("/", "")

    # Verifica se há mais de um arquivo a ser processado
    if row['arquivos'] > 1:
        for i in range(1, int(row['arquivos']) + 1):
            time.sleep(5)
            navegador = download_imagem_dentro_loop(
                navegador,
                path_generico_multiplo.format(partes_int, i),
                f"{caminho}\\{num_processo}",
                #f"{row.name}_{i}"
                f"{nome_documento}_{i}"
            )
    else:
        navegador = download_imagem_dentro_loop(
            navegador,
            path_generico_individual.format(partes_int),
            f"{caminho}\\{num_processo}",
            #row.name
            nome_documento
        )
    
    return navegador


def tentar_processar_linha(navegador, row, path_generico_multiplo, path_generico_individual, caminho, num_processo, posicoes_pagina):
    tentativas = 3
    for i in range(tentativas):
        try:
            navegador = processar_linha(
                navegador,
                row,
                path_generico_multiplo,
                path_generico_individual,
                caminho,
                num_processo,
                posicoes_pagina[i]
            )
            break  # Se a operação for bem-sucedida, sai do loop
        except Exception as e:
            print(f"Tentativa {i + 1} falhou com erro: {e}")
            if i == tentativas - 1:
                print("Todas as tentativas falharam.")
    return navegador


def download_automatico_processo_danos_eletricos(navegador):

    time.sleep(7)
    # Ir para página de envio dos documentos
    orcamento_botao = WebDriverWait(navegador, 15).until(
        EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-ressarcimento/app-footer/footer/button[6]'))
    )
    orcamento_botao.click()

    # Alterar o navegador para a aba de download de documentos
    WebDriverWait(navegador, 10).until(
        EC.number_of_windows_to_be(2))
    new_window_handle = navegador.window_handles[1]
    navegador.switch_to.window(new_window_handle)

    # Download de Formulário Cadastrais
    try:
        time.sleep(7)
        form_cadastral = WebDriverWait(navegador, 15).until(
            EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/ng-component/main/article/section[3]/app-files-upload/div/div[1]/div/app-tipo-documento/div/div[2]/app-documentos-ocorrencia/div/div/app-documento-ocorrencia-item/div/div[2]/a'))
        )
        form_cadastral.click()
    except:
        pass

    time.sleep(10)
    xpath_docs_adicionais = "/html/body/app-root/ng-component/main/article/section[3]/app-files-upload/div/div[2]/div[2]/div[1]"

    try:
        # Localizar o elemento pelo XPath
        element = navegador.find_element(By.XPATH, xpath_docs_adicionais)
        
    except Exception as e:
        print("Elemento não encontrado. Erro:", e)


    # Lista de documentos
    lista_documentos = ['Conta de Energia Elétrica em Nome do Segurado',
                        'Documento Pessoal do Segurado com CPF e RG',
                        'Foto da etiqueta com modelo e número de serie do equipamento danificado',
                        'Foto do número do registro do medidor de energia',
                        'Foto Frontal do Equipamento Danificado',
                        'Laudo Técnico',
                        'Nota Fiscal',
                        'Orçamento de Reparação/Reposição', 
                        'Solicitação de Documentos',
                        'Áudio de Regulação',
                        'Carta do segurado com descrição do evento',
                        'Carta do Terceiro com Descrição do Evento',
                        'Comprovante de Endereço em Nome do Terceiro',
                        'Comprovante Valor Aluguel',
                        'Documento de comprovação de propriedade do imóvel',
                        'Documento Pessoal do Terceiro com CPF e RG',
                        'E-mail - PROPERTY',
                        'E-mail Recebido - PROPERTY',
                        'Fotos do item danificado',
                        'Fotos do local do item',
                        'Fotos dos danos reclamados',
                        'Noticiário na Mídia',
                        'Relação dos bens subtraídos',
                        'RES - Comprovante de Despesa - PROPERTY',
                        'RES - Comprovante de Pagamento - PROPERTY',
                        'RES - Contestação',
                        'RES - Documentos Judiciais - PROPERTY',
                        'RES - Execução',
                        'RES - Nota Fiscal Pagamento Honório - PROPERTY',
                        'RES - Outros - PROPERTY',
                        'RES - Parecer Prestador',
                        'RES - Pesquisa Financeira',
                        'RES - Petição Inicial',
                        'RES - PROPERTY',
                        'RES - Recurso de Apelação',
                        'RES - Recurso Outros',
                        'RES - Sentença Desfavorável a Cia',
                        'RES - Sentença Favorável a Cia',
                        'RES - Termo de Transação - PROPERTY',
                        'Termo de Quitação Assinado pelo Terceiro']

    texto = element.text


    info_documentos = processar_texto(texto, lista_documentos)

    df_download = pd.DataFrame(info_documentos).T
    df_download = df_download.dropna()
    df_download = df_download.sort_values(by='partes')
    #df_download

    path_generico_individual = "/html/body/app-root/ng-component/main/article/section[3]/app-files-upload/div/div[2]/div[2]/div[1]/div[2]/div[{}]/app-tipo-documento/div/div[2]/app-documentos-ocorrencia/div/div/app-documento-ocorrencia-item/div/div[2]/a"
    path_generico_multiplo = "/html/body/app-root/ng-component/main/article/section[3]/app-files-upload/div/div[2]/div[2]/div[1]/div[2]/div[{}]/app-tipo-documento/div/div[2]/app-documentos-ocorrencia/div[{}]/div/app-documento-ocorrencia-item/div/div[2]/a"

    posicoes_pagina = [300, 500, 700]

    # Seu loop para iterar sobre as linhas do DataFrame
    for i, row in df_download.iterrows():

        # Download de documento
        time.sleep(5)

        # Realizando downloads
        navegador = tentar_processar_linha(navegador, row, path_generico_multiplo, path_generico_individual, caminho, num_processo, posicoes_pagina)
        #navegador = processar_linha(navegador, row, path_generico_multiplo, path_generico_individual, caminho, num_processo, posicoes_pagina[1])
            
    
    navegador.quit()