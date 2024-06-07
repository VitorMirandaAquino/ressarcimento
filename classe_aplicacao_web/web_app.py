import streamlit as st
#from functions import configurar_navegador_para_download, realizar_login_liberty, localizar_processo
#from functions_auto import baixar_orcamento, downloads, processos_auto_pipeline
from functions_danos_eletricos import pipeline_danos_eletricos
import pandas as pd
from classe_navegador import LibertyAutomation
from classe_auto.procedimentos import Procedimentos

class WebApp:
    def __init__(self):
        self.login_credencial = None
        self.senha_credencial = None
        self.caminho = r"C:\Users\Vitor\Documents\Repositórios\automação\ressarcimento\dados"
        self.tipo_processo = None

    def run(self):
        st.set_page_config(
            page_title="Download de documentos",
            page_icon=":page_facing_up:"
        )

        st.title("Download de documentos :page_facing_up:")
        st.header("Configuração para download")
        self.get_credenciais()
        self.select_caminho()
        self.select_tipo_processo()

        if self.login_credencial and self.senha_credencial and self.tipo_processo:
            if self.tipo_processo == "AUTO":
                self.processos_auto_pipeline()
            elif self.tipo_processo == "DANOS ELÉTRICOS":
                pipeline_danos_eletricos(caminho=self.caminho, login=self.login_credencial, senha=self.senha_credencial)

    def get_credenciais(self):
        self.login_credencial = st.text_input("Digite o login do site:")
        self.senha_credencial = st.text_input("Digite a senha do site:", type="password")

    def select_caminho(self):
        st.subheader("Caminho para salvar")
        st.write(self.caminho)

    def select_tipo_processo(self):
        st.subheader("Tipo de Processo")
        self.tipo_processo = st.selectbox("Você deseja baixar as informações de qual tipo de Processo?", ("AUTO", "DANOS ELÉTRICOS"))

    def processos_auto_pipeline(self):
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
                    navegador = LibertyAutomation(self.caminho, processo)  # Instanciando a classe LibertyAutomation
                    #navegador.configurar_navegador_para_download(self.caminho, processo)
                    st.write("Configuração concluída")
                    navegador.realizar_login_liberty(self.login_credencial, self.senha_credencial)
                    st.write("Login concluído.")
                    navegador.localizar_processo()
                    
                    procedimentos = Procedimentos(navegador)  # Instanciando a classe Procedimentos

                    if opcao_orcamento == "Sim":
                        try:
                            procedimentos.baixar_orcamento()
                            st.write("Download do orçamento concluído.")
                        except:
                            navegador.fechar_navegador()
                            lista_docs_problema.append(processo)
                            st.write("Problema no download do orçamento.")
                            navegador = LibertyAutomation(self.caminho, processo)  # Reinstancia o navegador
                            #navegador = procedimentos.configurar_navegador_para_download(self.caminho, processo)
                            navegador.realizar_login_liberty(self.login_credencial, self.senha_credencial)
                            navegador.localizar_processo()
                            procedimentos = Procedimentos(navegador)

                    documentos_baixados, flag_problema = procedimentos.downloads()
                    if flag_problema:
                        lista_docs_problema.append(processo)
                    lista_docs_baixados.append(documentos_baixados)
                    st.write("Download dos documentos concluído.")

            st.subheader("Geral")
            df_processo_show['Documentos Baixados'] = lista_docs_baixados
            st.table(df_processo_show)

            for doc in lista_docs_problema:
                st.warning(f'Problema no download no processo {str(doc)}', icon="⚠️")

            st.button('Rerun')
