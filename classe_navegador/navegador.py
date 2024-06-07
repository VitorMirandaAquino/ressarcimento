from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class LibertyAutomation:
    def __init__(self, caminho, num_processo):
        self.caminho = caminho
        self.num_processo = num_processo
        self.navegador = self.configurar_navegador_para_download()

    def configurar_navegador_para_download(self):
        servico = Service(ChromeDriverManager().install())
        chrome_options = webdriver.ChromeOptions()
        download_directory = self.caminho + f"\\{str(self.num_processo)}"
        prefs = {
            "download.default_directory": download_directory,
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "plugins.always_open_pdf_externally": True,
            "profile.default_content_settings.images": 1
        }
        chrome_options.add_experimental_option("prefs", prefs)
        navegador = webdriver.Chrome(service=servico, options=chrome_options)
        return navegador

    def realizar_login_liberty(self, login, senha):
        self.navegador.get("https://ressarcimentofianca.libertyseguros.com.br/login")
        self.navegador.maximize_window()
        self.enviar_valor_para_campo(By.XPATH, '/html/body/app-root/app-login-prestador/div[2]/div/div/div[2]/div[2]/div/div[1]/input', login)
        self.enviar_valor_para_campo(By.XPATH, '/html/body/app-root/app-login-prestador/div[2]/div/div/div[2]/div[2]/div/div[2]/input', senha)
        self.clicar_botao(By.XPATH, '/html/body/app-root/app-login-prestador/div[2]/div/div/div[2]/div[2]/div/div[3]/input')

    def localizar_processo(self):
        self.enviar_valor_para_campo(By.XPATH, '//*[@id="pesquisa"]', self.num_processo)
        self.clicar_botao(By.XPATH, '/html/body/app-root/app-pesquisa/div[2]/div[3]/div[2]/button[1]')

    def clicar_botao(self, by, valor):
        botao = WebDriverWait(self.navegador, 10).until(
            EC.element_to_be_clickable((by, valor))
        )
        botao.click()

    def enviar_valor_para_campo(self, by, valor, texto):
        campo = WebDriverWait(self.navegador, 10).until(
            EC.presence_of_element_located((by, valor))
        )
        campo.send_keys(texto)

    def mudar_para_aba(self, numero_aba):
        WebDriverWait(self.navegador, 10).until(
            EC.number_of_windows_to_be(numero_aba + 1)
        )
        new_window_handle = self.navegador.window_handles[numero_aba]
        self.navegador.switch_to.window(new_window_handle)

    def fechar_aba(self):
        self.navegador.close()
        WebDriverWait(self.navegador, 10).until(
            EC.number_of_windows_to_be(len(self.navegador.window_handles))
        )
        new_window_handle = self.navegador.window_handles[-1]
        self.navegador.switch_to.window(new_window_handle)

    def executar_script(self, script , element):
        self.navegador.execute_script(script, element)

