import streamlit as st
from functions import configurar_navegador_para_download, realizar_login_liberty, localizar_processo
from functions_auto import baixar_orcamento, downloads, processos_auto_pipeline
import pandas as pd

st.set_page_config(
        page_title="Download de documentos",
        page_icon=":page_facing_up:"
    )

st.title("Download de documentos :page_facing_up:")
st.header("Configuração para download")
st.subheader("Credenciais")
login_credencial = st.text_input("Digite o login do site:", value=None)
senha_credencial = st.text_input("Digite a senha do site:", value=None)

if login_credencial is not None and senha_credencial is not None:
    st.subheader("Caminho para salvar")
    #caminho = st.text_input("Digite o caminho para serem salvados os arquivos: [Usar duas barras ao invés de uma só]", value=None)
    caminho = r'C:\Users\vmaqu\OneDrive\Documentos\Repositórios\ressarcimento\dados'

    if caminho is not None:
        st.write(caminho)

        st.subheader("Tipo de Procesoo")
        tipo_processo = st.selectbox("Você deseja baixar as informações de qual tipo de Processo?", ("AUTO", "DANOS ELÉTRICOS"))

        if tipo_processo == "AUTO":
            processos_auto_pipeline(caminho, login_credencial, senha_credencial)
        elif tipo_processo == "DANOS ELÉTRICOS":
            
