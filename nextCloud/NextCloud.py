import requests
import os

# Configurações
URL_NEXTCLOUD = 'https://seu.nextcloud.com'  # Substitua pelo URL do seu servidor Nextcloud
USUARIO = 'seu_usuario'
SENHA = 'sua_senha'
PASTA_NEXTCLOUD = '/remote.php/dav/files/seu_usuario/sua_pasta'  # Substitua pelo caminho da pasta no seu Nextcloud

# Função para baixar arquivos do Nextcloud
def baixar_arquivos_do_nextcloud():
    # Criando a sessão e autenticando
    session = requests.Session()
    session.auth = (USUARIO, SENHA)

    # Obtendo a lista de arquivos na pasta
    url_listar_arquivos = f"{URL_NEXTCLOUD}{PASTA_NEXTCLOUD}"
    response = session.request('PROPFIND', url_listar_arquivos)
    
    # Processar a resposta para obter os nomes dos arquivos
    arquivos = []
    if response.status_code == 207:
        namespace = {'d': 'DAV:'}
        xml_response = response.content.decode('utf-8')
        for linha in xml_response.split('\n'):
            if '<d:href>' in linha:
                arquivo = linha.strip().replace('<d:href>', '').replace('</d:href>', '').replace(PASTA_NEXTCLOUD, '')
                arquivos.append(arquivo)

    # Baixar cada arquivo
    for arquivo in arquivos:
        url_arquivo = f"{URL_NEXTCLOUD}{PASTA_NEXTCLOUD}/{arquivo}"
        response = session.get(url_arquivo)
        caminho_local = os.path.join('downloads', arquivo)  # Define o caminho local para salvar o arquivo
        with open(caminho_local, 'wb') as arquivo_local:
            arquivo_local.write(response.content)

    print("Download concluído.")

if __name__ == "__main__":
    baixar_arquivos_do_nextcloud()
