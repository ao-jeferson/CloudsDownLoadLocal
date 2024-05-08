import dropbox
import os

# Configurações
ACCESS_TOKEN = 'seu_access_token_do_dropbox'
PASTA_DO_DROPBOX = '/pasta/que/contem/os/arquivos'

# Função para baixar arquivos do Dropbox
def baixar_arquivos_do_dropbox():
    dbx = dropbox.Dropbox(ACCESS_TOKEN)

    # Lista todos os arquivos na pasta do Dropbox
    for entry in dbx.files_list_folder(PASTA_DO_DROPBOX).entries:
        # Verifica se o item é um arquivo (exclui pastas)
        if isinstance(entry, dropbox.files.FileMetadata):
            # Baixa o arquivo
            caminho_local = os.path.join('downloads', entry.name)  # Define o caminho local para salvar o arquivo
            with open(caminho_local, 'wb') as arquivo_local:
                metadata, conteudo = dbx.files_download(entry.path_lower)
                arquivo_local.write(conteudo.content)

    print("Download concluído.")

if __name__ == "__main__":
    baixar_arquivos_do_dropbox()
