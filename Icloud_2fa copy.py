from pyicloud import PyiCloudService
from time import sleep

# Função para solicitar o código de verificação de dois fatores via SMS
def request_verification_code(api):
    api.send_verification_code()

# Função para fazer login no iCloud com autenticação de dois fatores
def icloud_login(username, password, sms_verification_callback):
    api = PyiCloudService(username, password)
    if api.requires_2fa:
        # Se a autenticação de dois fatores for necessária
        if not api.trusted_devices:
            raise Exception("Não foi possível encontrar um dispositivo confiável.")
        
        # Solicitar código de verificação
        sms_verification_callback(api)

        # Esperar até que o código seja inserido
        while True:
            code = input("Insira o código de verificação: ")
            if api.validate_verification_code(code):
                break
            else:
                print("Código incorreto. Tente novamente.")
    return api

# Função para baixar todos os arquivos de uma pasta
def download_icloud_files(api, folder_name, destination_path):
    folder = api.drive[folder_name]
    for item in folder:
        if item.type == 'file':
            item.download(destination_path)

# Informações de login
username = "jeferson.ao@icloud.com"
password = "slk350@K"

try:
    # Fazendo login
    api = icloud_login(username, password, request_verification_code)

    # Baixar arquivos da pasta desejada
    download_icloud_files(api, "nome_da_pasta", "/caminho/para/salvar/os/arquivos")

    print("Arquivos baixados com sucesso!")
except Exception as e:
    print("Ocorreu um erro:", e)
