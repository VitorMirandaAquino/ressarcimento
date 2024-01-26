import streamlit as st
from functions import configurar_navegador_para_download, realizar_login_liberty, localizar_processo, baixar_orcamento, downloads
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
    caminho = r'C:\Users\Vitor\Documents\Repositórios\automação\ressarcimento\dados'

    if caminho is not None:
        st.write(caminho)

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
                    navegador = realizar_login_liberty(navegador, login_credencial, senha_credencial)

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
                            navegador = realizar_login_liberty(navegador, login_credencial, senha_credencial)
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