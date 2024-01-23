from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
#from credenciais import login_allianz, senha_allianz
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import UnexpectedAlertPresentException
import streamlit as st

def configuracao(caminho, num_processo):
    servico = Service(ChromeDriverManager().install())

    # Set up Chrome options
    chrome_options = webdriver.ChromeOptions()

    # Specify the download directory
    download_directory = caminho + f"\\{str(num_processo)}"
    # Adicione a opção de preferência
    prefs = {"download.default_directory": download_directory}
    chrome_options.add_experimental_option("prefs", prefs)

    navegador =  webdriver.Chrome(service=servico, options=chrome_options)

    return navegador


def login(navegador, login_allianz, senha_allianz):
    # Indo para o site da liberty
    navegador.get(url="https://ressarcimentofianca.libertyseguros.com.br/login")

    time.sleep(3)
    # Inserindo login
    navegador.find_element('xpath', '/html/body/app-root/app-login-prestador/div[2]/div/div/div[2]/div[2]/div/div[1]/input').send_keys(login_allianz)
    # Inserindo senha
    navegador.find_element('xpath', '/html/body/app-root/app-login-prestador/div[2]/div/div/div[2]/div[2]/div/div[2]/input').send_keys(senha_allianz)

    time.sleep(3)
    # Logando no conta
    navegador.find_element('xpath', '/html/body/app-root/app-login-prestador/div[2]/div/div/div[2]/div[2]/div/div[3]/input').click()

    return navegador





def downloads(navegador, num_processo):
    # Adicionando o número do processo
    search_box = WebDriverWait(navegador, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="pesquisa"]'))
    )
    search_box.send_keys(num_processo)

    # Pesquisando o processo
    search_button = WebDriverWait(navegador, 10).until(
        EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-pesquisa/div[2]/div[3]/div[2]/button[1]'))
    )
    search_button.click()

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

    time.sleep(5)
    # Descendo para o final da página
    #navegador.execute_script("window.scrollTo(0, 10);")
    time.sleep(5)


    documentos_baixados = 0
    
    flag_problema = False
    for i in range(2, 20):
        time.sleep(3)

        try:
            navegador.execute_script("window.scrollTo(0, 5);")
        except UnexpectedAlertPresentException as e:
            #st.write(e)
            flag_problema = True
            break
            # Handle the alert here, for example, by accepting it
            #alert = navegador.switch_to.alert
            #alert.accept()

        element_xpath = f'//*[@id="documento-necessario"]/div[{i}]/div[2]/div/div'
        
        try:
            # Wait for the element to be clickable
            element = WebDriverWait(navegador, 10).until(
                EC.element_to_be_clickable((By.XPATH, element_xpath))
            )

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

