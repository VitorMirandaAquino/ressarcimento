from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import UnexpectedAlertPresentException, TimeoutException

import time

import pandas as pd
import numpy as np
import re
import streamlit as st

import requests
import os

from classe_navegador.navegador import LibertyAutomation

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

path_generico_individual = "/html/body/app-root/ng-component/main/article/section[3]/app-files-upload/div/div[2]/div[2]/div[1]/div[2]/div[{}]/app-tipo-documento/div/div[2]/app-documentos-ocorrencia/div/div/app-documento-ocorrencia-item/div/div[2]/a"
path_generico_multiplo = "/html/body/app-root/ng-component/main/article/section[3]/app-files-upload/div/div[2]/div[2]/div[1]/div[2]/div[{}]/app-tipo-documento/div/div[2]/app-documentos-ocorrencia/div[{}]/div/app-documento-ocorrencia-item/div/div[2]/a"


class Procedimentos:
    def __init__(self, liberty_automation: LibertyAutomation):
        self.liberty_automation = liberty_automation
        self.lista_documentos = lista_documentos
        self.xpath_generico_individual = path_generico_individual
        self.xpath_generico_multiplo = path_generico_multiplo
        

    def ir_para_pagina_downloads(self):
        time.sleep(7)

        # Ir para página de envio dos documentos
        self.liberty_automation.clicar_botao(By.XPATH, '/html/body/app-root/app-ressarcimento/app-footer/footer/button[6]')

        # Alterar o navegador para a aba de download de documentos
        self.liberty_automation.mudar_para_aba(1)

    def download_formularios_cadastrais(self):
        time.sleep(7)
        try:
            self.liberty_automation.clicar_botao(By.XPATH, '/html/body/app-root/ng-component/main/article/section[3]/app-files-upload/div/div[1]/div/app-tipo-documento/div/div[2]/app-documentos-ocorrencia/div/div/app-documento-ocorrencia-item/div/div[2]/a')
        except:
            pass
        time.sleep(5)

    def localizar_elemento_documentos(self):
        xpath_docs_adicionais = "/html/body/app-root/ng-component/main/article/section[3]/app-files-upload/div/div[2]/div[2]/div[1]"

        try:
            # Localizar o elemento pelo XPath
            element = self.liberty_automation.navegador.find_element(By.XPATH, xpath_docs_adicionais)
            return element.text
        except Exception as e:
            print("Elemento não encontrado. Erro:", e)

    def processar_texto(self):
        """
        Processa o texto para encontrar o número de arquivos adicionados para cada documento na lista de documentos.

        Returns:
        dict: Um dicionário com a contagem de arquivos e as partes do texto para cada documento.
        """
        texto = self.localizar_elemento_documentos()

        # Quebrar o texto em partes após "arquivo adicionado"
        partes_texto = re.split(r'arquivo[s]? adicionado[s]?', texto)

        # Dicionário para armazenar a contagem de documentos e o número de arquivos
        info_documentos = {doc: {'arquivos': 0, 'partes': np.nan} for doc in self.lista_documentos}

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

        df_download = pd.DataFrame(info_documentos).T
        df_download = df_download.dropna()
        df_download = df_download.sort_values(by='partes')

        return df_download
    
    def download_imagem_dentro_loop(self, xpath, nome_arquivo):
        
        time.sleep(3)

        for _ in range(0,3):

            try:
                self.liberty_automation.clicar_botao(By.XPATH, xpath)
                break
            except:
                self.liberty_automation.rolar_pagina()
                pass
    

        try:        
            # Alterar o navegador para a aba de download de documentos
            WebDriverWait(self.liberty_automation.navegador, 20).until(
                EC.number_of_windows_to_be(3))
        except TimeoutException as e: 
            print(f'Erro: {e}')
            time.sleep(5)

        
        time.sleep(5)

        # Obtenha uma lista de identificadores de janelas
        janelas_abertas = self.liberty_automation.navegador.window_handles

        # Determine o número de janelas abertas
        numero_janelas = len(janelas_abertas)

        if numero_janelas > 2:

            self.liberty_automation.mudar_para_aba(2)

            # Obtenha a URL da imagem
            url_imagem = self.liberty_automation.navegador.current_url

            time.sleep(5)

            self.liberty_automation.navegador.close()

            # Volte para a janela anterior
            self.liberty_automation.navegador.switch_to.window(self.liberty_automation.navegador.window_handles[1])

            # Baixe a imagem usando requests
            response = requests.get(url_imagem)

            # Verifique se a solicitação foi bem-sucedida (código de status 200)
            if response.status_code == 200:

                # Verifique se o diretório de salvamento existe, se não, crie
                if not os.path.exists(self.liberty_automation.caminho):
                    os.makedirs(self.liberty_automation.caminho)
                
                # Salve a imagem localmente no diretório especificado
                with open(os.path.join(f"{self.liberty_automation.caminho}\\{self.liberty_automation.num_processo}", f"{nome_arquivo}.jpg"), "wb") as file:
                    file.write(response.content)
            else:
                print("Não foi possível baixar a imagem.")
    


    def processar_linha(self, row):
        # Converte row['partes'] para inteiro antes de usar na operação matemática
        partes_int = int(row['partes'])
        nome_documento = row.name
        nome_documento = nome_documento.replace("/", "")


        # Verifica se há mais de um arquivo a ser processado
        if row['arquivos'] > 1:
            for i in range(1, int(row['arquivos']) + 1):
                time.sleep(5)
                self.download_imagem_dentro_loop(
                    self.xpath_generico_multiplo.format(partes_int, i),
#                    f"{self.liberty_automation.caminho}\\{self.liberty_automation.num_processo}",
                    f"{nome_documento}_{i}"
                )
        else:
            self.download_imagem_dentro_loop(
                self.xpath_generico_individual.format(partes_int),
#                f"{self.liberty_automation.caminho}\\{self.liberty_automation.num_processo}",
                nome_documento
            )
        

