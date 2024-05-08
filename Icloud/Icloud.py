from pyicloud import PyiCloudService
import os

# Autenticação no iCloud
api_icloud = PyiCloudService('seu_email_icloud', 'sua_senha_icloud')

# Diretório onde os arquivos serão salvos
download_directory = 'caminho/para/salvar/os/arquivos'

# Verifica se o diretório de download existe, se não, cria
if not os.path.exists(download_directory):
    os.makedirs(download_directory)

# Função para baixar um arquivo do iCloud
def download_icloud_file(file_id, file_name):
    file_data = api_icloud.drive.download(file_id)
    file_path = os.path.join(download_directory, file_name)
    with open(file_path, 'wb') as f:
        f.write(file_data)

# Obtém a lista de arquivos do iCloud
icloud_files = api_icloud.drive.get_list()

# Baixa cada arquivo do iCloud
for file in icloud_files:
    file_id = file['id']
    file_name = file['name']
    download_icloud_file(file_id, file_name)
    print(f"Arquivo '{file_name}' baixado com sucesso.")

print("Todos os arquivos foram baixados.")
