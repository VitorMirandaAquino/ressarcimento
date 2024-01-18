from functions import configuracao, login, downloads

num_processo = 16075488
caminho = r"C:\Users\Vitor\Documents\Repositórios\automação\ressarcimento\dados"

navegador = configuracao(caminho, num_processo)
navegador = login(navegador)
downloads(navegador, num_processo)

