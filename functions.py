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

