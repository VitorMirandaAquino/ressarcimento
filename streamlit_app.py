from classe_aplicacao_web.web_app import WebApp
import streamlit as st
import os

if __name__ == "__main__":


    @st.experimental_singleton
    def install_chrome_driver():
        os.system('apt-get update')
        os.system('apt-get install -y chromium-driver')
        os.system('ln -s /usr/lib/chromium-browser/chromedriver /usr/bin/chromedriver')

    install_chrome_driver()

    app = WebApp()
    app.run()