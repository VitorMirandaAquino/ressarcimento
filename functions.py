from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
#from credenciais import login_allianz, senha_allianz
import time


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

    navegador.get(url="https://ressarcimentofianca.libertyseguros.com.br/login")

    time.sleep(1.5)
    navegador.find_element('xpath', '/html/body/app-root/app-login-prestador/div[2]/div/div/div[2]/div[2]/div/div[1]/input').send_keys(login_allianz)
    navegador.find_element('xpath', '/html/body/app-root/app-login-prestador/div[2]/div/div/div[2]/div[2]/div/div[2]/input').send_keys(senha_allianz)

    time.sleep(1)
    navegador.find_element('xpath', '/html/body/app-root/app-login-prestador/div[2]/div/div/div[2]/div[2]/div/div[3]/input').click()

    return navegador

def downloads(navegador, num_processo):
    time.sleep(2)
    navegador.find_element('xpath', '//*[@id="pesquisa"]').send_keys(num_processo)

    time.sleep(0.5)
    navegador.find_element('xpath', '/html/body/app-root/app-pesquisa/div[2]/div[3]/div[2]/button[1]').click()

    time.sleep(3)
    navegador.find_element('xpath', '/html/body/app-root/app-ressarcimento/app-footer/footer/button[6]').click()

    time.sleep(10)
    # Switch to the new window
    new_window_handle = navegador.window_handles[1]  # Assumes the new window is the second in the list
    navegador.switch_to.window(new_window_handle)

    time.sleep(2)
    navegador.execute_script("window.scrollTo(0, 1000);")
    navegador.find_element('xpath', '/html/body/form/div[3]/div/div[1]/div[3]/div[1]/div[5]/div/div[2]/div[2]/div/div').click()

    time.sleep(3)
    navegador.find_element('xpath', '/html/body/form/div[3]/div/div[1]/div[3]/div[1]/div[5]/div/div[3]/div[2]/div/div').click()

    time.sleep(3)
    navegador.find_element('xpath', '/html/body/form/div[3]/div/div[1]/div[3]/div[1]/div[5]/div/div[4]/div[2]/div/div').click()

    time.sleep(2)
    # Close the new window
    navegador.close()

    time.sleep(1)
    # Switch back to the original window
    navegador.switch_to.window(navegador.window_handles[0])

    # Close the original window
    navegador.quit()

