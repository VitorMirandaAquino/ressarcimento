import streamlit as st
from functions import configuracao, login, downloads



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
        st.subheader("Processo")
        num_processo = st.text_input(label="Digite o número do processo:", value=None)
        st.write(num_processo)

        if num_processo is not None:
            num_processo = int(num_processo)
            with st.status("Fazendo downloand dos arquivos..."):
                navegador = configuracao(caminho, num_processo)
                st.write("Configuração concluída")
                navegador = login(navegador)
                st.write("Login concluído.")
                downloads(navegador, num_processo)
                st.write("Download concluído.")

            #num_processo = 16075488
            #caminho = r"C:\Users\Vitor\Documents\Repositórios\automação\ressarcimento\dados"


                


            st.button('Rerun')
            #st.write(repr(caminho))
