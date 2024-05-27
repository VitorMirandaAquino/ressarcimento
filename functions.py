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

def configurar_navegador_para_download(caminho, num_processo):
    """
    Configura e inicializa um navegador Chrome para automatizar o download de arquivos.
    
    Parâmetros:
    caminho (str): Caminho base onde os arquivos serão baixados.
    num_processo (str): Identificador do processo, usado para criar uma subpasta no caminho de download.

    Retorna:
    webdriver.Chrome: Uma instância do navegador Chrome configurada com as opções de download especificadas.
    
    Esta função instala o ChromeDriver, configura as opções de download para o navegador
    Chrome e retorna a instância do navegador. O diretório de download é definido como uma
    subpasta dentro do caminho fornecido, baseado no número do processo.
    """

    # Instala o ChromeDriver e inicializa o serviço
    servico = Service(ChromeDriverManager().install())

    # Configura as opções do navegador Chrome
    chrome_options = webdriver.ChromeOptions()

    # Especifica o diretório de download com base no caminho e número do processo
    download_directory = caminho + f"\\{str(num_processo)}"

    # Define as preferências de download para o navegador
    prefs = {
        "download.default_directory": download_directory,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "plugins.always_open_pdf_externally": True,
        "profile.default_content_settings.images": 1
    }
    chrome_options.add_experimental_option("prefs", prefs)

    # Inicializa o navegador Chrome com as opções configuradas
    navegador = webdriver.Chrome(service=servico, options=chrome_options)

    return navegador

def realizar_login_liberty(navegador, login, senha):
    """
    Realiza o login no site da Liberty Seguros.

    Parâmetros:
    navegador (webdriver.Chrome): Uma instância do navegador Chrome.
    login (str): Nome de usuário para login.
    senha (str): Senha para login.

    Retorna:
    webdriver.Chrome: A instância do navegador com a sessão de login iniciada.

    Esta função acessa o site de ressarcimento da Liberty Seguros, aguarda a presença dos elementos
    de login e senha, insere as credenciais e realiza o login.
    """

    # Acessa o site da Liberty Seguros
    navegador.get("https://ressarcimentofianca.libertyseguros.com.br/login")

    # Abrir tela cheia
    navegador.maximize_window()

    # Espera pela presença do campo de login e insere o login
    WebDriverWait(navegador, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/app-root/app-login-prestador/div[2]/div/div/div[2]/div[2]/div/div[1]/input'))).send_keys(login)

    # Espera pela presença do campo de senha e insere a senha
    WebDriverWait(navegador, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/app-root/app-login-prestador/div[2]/div/div/div[2]/div[2]/div/div[2]/input'))).send_keys(senha)

    # Espera pela presença do botão de login e clica nele
    WebDriverWait(navegador, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/app-root/app-login-prestador/div[2]/div/div/div[2]/div[2]/div/div[3]/input'))).click()

    return navegador

def localizar_processo(navegador, num_processo):
    """
    Localiza um processo no site especificado, utilizando o número do processo.

    Parâmetros:
    navegador (webdriver.Chrome): Uma instância do navegador Chrome.
    num_processo (str): Número do processo a ser pesquisado.

    Retorna:
    webdriver.Chrome: A instância do navegador após a pesquisa do processo.

    Esta função aguarda a presença do campo de pesquisa, insere o número do processo,
    aguarda a presença do botão de pesquisa e clica nele para realizar a busca.
    """

    # Aguarda pela presença do campo de pesquisa e insere o número do processo
    search_box = WebDriverWait(navegador, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="pesquisa"]'))
    )
    search_box.send_keys(num_processo)

    # Aguarda pela presença do botão de pesquisa e clica nele
    search_button = WebDriverWait(navegador, 10).until(
        EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-pesquisa/div[2]/div[3]/div[2]/button[1]'))
    )
    search_button.click()

    return navegador





