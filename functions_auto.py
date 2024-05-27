from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import UnexpectedAlertPresentException
import streamlit as st
import pandas as pd
from functions import configurar_navegador_para_download, realizar_login_liberty, localizar_processo


def baixar_orcamento(navegador):
    """
    Navega em um site específico e automatiza o processo de download de orçamentos e fotos.

    Parâmetros:
    navegador (webdriver.Chrome): Uma instância do navegador Chrome controlada pelo Selenium.

    O processo inclui:
    - Clicar no botão para ir à página de orçamento.
    - Aguardar e clicar no botão de relatório completo, o que abre uma nova aba.
    - Mudar para a nova aba e clicar no botão de download do PDF do orçamento.
    - Esperar a finalização do download e fechar a aba.
    - Retornar para a aba anterior e clicar no botão de visualização de fotos do orçamento.
    - Selecionar todas as fotos disponíveis e iniciar o download.
    - Fechar a aba de fotos e retornar para a aba original.

    Retorna:
    webdriver.Chrome: A instância do navegador após a execução das operações de download.

    Notas:
    - A função utiliza `time.sleep` para intervalos fixos entre as operações, o que pode ser
      substituído por esperas mais dinâmicas do Selenium em futuras otimizações.
    - A função depende da estrutura específica do site e dos seletores XPATH utilizados, o que
      pode requerer ajustes caso haja mudanças no layout ou no comportamento do site.
    """
    
    time.sleep(7)
    # Ir para página de orçamento
    orcamento_botao = WebDriverWait(navegador, 15).until(
        EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-ressarcimento/app-footer/footer/button[4]'))
    )
    orcamento_botao.click()

    time.sleep(5)
    # Alterar o navegador para a segunda aba
    WebDriverWait(navegador, 10).until(
        EC.number_of_windows_to_be(2))
    new_window_handle = navegador.window_handles[1]
    navegador.switch_to.window(new_window_handle)

    #time.sleep(7)
    # Clicar no botão de relatório completo
    relatorio_botao = WebDriverWait(navegador, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="budget_report"]/div/div[2]/a/center')))
    relatorio_botao.click()


    # Alterar o navegador para terceira aba
    WebDriverWait(navegador, 10).until(
        EC.number_of_windows_to_be(3))
    new_window_handle = navegador.window_handles[2]
    navegador.switch_to.window(new_window_handle)

    # Clicar no botão de PDF
    relatorio_pdf_botao = WebDriverWait(navegador, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="btn_pdf_report"]')))
    relatorio_pdf_botao.click()

    time.sleep(8)

    # Fechar a terceira aba
    navegador.close()

    # Retornar para a segunda a aba
    WebDriverWait(navegador, 10).until(
        EC.number_of_windows_to_be(2))
    new_window_handle = navegador.window_handles[1]
    navegador.switch_to.window(new_window_handle)


    # Clicar no botão de fotos
    orcamento_fotos_botao = WebDriverWait(navegador, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="photos_menu"]')))
    orcamento_fotos_botao.click()

    time.sleep(5)


    # Clicar no botão para selecionar todas as fotos
    todas_fotos_botao = WebDriverWait(navegador, 20).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="budgeting-photos-content"]/div[1]/div[2]/div/label')))
    todas_fotos_botao.click()

    # Fazer o download das fotos
    baixar_fotos_botao = WebDriverWait(navegador, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="budgeting-photos-print"]/div/a[2]')))
    baixar_fotos_botao.click()

    time.sleep(8)

    # Fechar a segunda aba
    navegador.close()

    # Retornar para primeira aba
    WebDriverWait(navegador, 10).until(
        EC.number_of_windows_to_be(1))
    new_window_handle = navegador.window_handles[0]
    navegador.switch_to.window(new_window_handle)


    return navegador

def downloads(navegador):

    # Indo para o site com os arquivos
    files_button = WebDriverWait(navegador, 10).until(
        EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-ressarcimento/app-footer/footer/button[6]'))
    )
    files_button.click()
    

    # Mudando para aba com os documentos
    WebDriverWait(navegador, 10).until(
        EC.number_of_windows_to_be(2)
    )
    new_window_handle = navegador.window_handles[1]
    navegador.switch_to.window(new_window_handle)

    time.sleep(10)

    documentos_baixados = 0
    
    flag_problema = False
    for i in range(2, 20):
        time.sleep(3)
        element_xpath = f'//*[@id="documento-necessario"]/div[{i}]/div[2]/div/div'

        try:
            navegador.execute_script("window.scrollTo(0, 5);")
        except UnexpectedAlertPresentException as e:
            #st.write(e)
            flag_problema = True
            break
        try:
            # Wait for the element to be clickable
            element = WebDriverWait(navegador, 10).until(
                EC.element_to_be_clickable((By.XPATH, element_xpath)))
            # Scroll into view (just in case)
            navegador.execute_script("arguments[0].scrollIntoView(true);", element)
            # Click the element
            element.click()
            documentos_baixados += 1
            #st.write(i)
        except Exception as e:
            #st.write(e)
            break

    time.sleep(2)
    # Close the original window
    navegador.quit()

    return documentos_baixados, flag_problema

def processos_auto_pipeline(caminho, login, senha):
            
        st.subheader("Orçamento")
        opcao_orcamento = st.selectbox("Você deseja baixar as informações do orçamento?", ("Não", "Sim"))

        st.subheader("Processo")
        excel_file = st.file_uploader('Insira um arquivo com o número dos processos', type='xlsx')

        if excel_file is not None:
            df_processo = pd.read_excel(excel_file)
            df_processo_show = df_processo.copy()
            df_processo_show['Processo'] = df_processo_show['Processo'].astype('str')

            st.subheader("Procedimento")
            lista_docs_baixados = []
            lista_docs_problema = []
            with st.status("Fazendo download dos arquivos ..."):
                
                for processo in df_processo.Processo:

                    st.write(f'**Iniciando procedimento para o processo: {processo}**')
                    navegador = configurar_navegador_para_download(caminho, processo)

                    st.write("Configuração concluída")
                    navegador = realizar_login_liberty(navegador, login, senha)

                    st.write("Login concluído.")
                    navegador = localizar_processo(navegador, processo)

                    if opcao_orcamento == "Sim":
                        try:
                            navegador = baixar_orcamento(navegador)
                            st.write("Download do orçamento concluído.")
                        except:
                            navegador.quit()
                            lista_docs_problema.append(processo)
                            st.write("Problema no download do orçamento.")
                            navegador = configurar_navegador_para_download(caminho, processo)
                            navegador = realizar_login_liberty(navegador, login, senha)
                            navegador = localizar_processo(navegador, processo)


                    documentos_baixados, flag_problema = downloads(navegador)
                    if flag_problema  == True:
                        lista_docs_problema.append(processo)
                    lista_docs_baixados.append(documentos_baixados)
                    st.write("Download dos documentos concluído.")

                    
            st.subheader("Geral")
            df_processo_show['Documentos Baixados'] = lista_docs_baixados
            st.table(df_processo_show)

            for doc in lista_docs_problema:
                st.warning(f'Problema no download no processo {str(doc)}', icon="⚠️")

            st.button('Rerun')