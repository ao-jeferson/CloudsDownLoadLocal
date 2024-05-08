import sys
import click
from pyicloud import PyiCloudService
import os
import datetime

try:
    # Autenticação no iCloud via sms
    print("Setup Time Zone")
    datetime.datetime.now().strftime("%X %x %Z")
    os.environ["TZ"] = "Brazil, America/Sao_Paulo"

    api = PyiCloudService('jeferson.ao@icloud.com', 'slk350@K')
    if api.requires_2fa:         
     print("Two-factor authentication required. Your trusted devices are:")

    devices = api.trusted_devices    
    for i, device in enumerate(devices):
        print(
            "  %s: %s"
            % (i, device.get("deviceName", "SMS to %s" % device.get("phoneNumber")))
        )

    device = click.prompt("Which device would you like to use?", default=0)
    device = devices[device]
    if not api.send_verification_code(device):
        print("Failed to send verification code")
        sys.exit(1)

    code = click.prompt("Please enter validation code")
    if not api.validate_verification_code(device, code):
        print("Failed to verify verification code")
        sys.exit(1)


    # Diretório onde os arquivos serão salvos
    download_directory = 'C:\\temp\\'

    # Verifica se o diretório de download existe, se não, cria
    if not os.path.exists(download_directory):
        os.makedirs(download_directory)

    # Função para baixar um arquivo do iCloud
    def download_icloud_file(file_id, file_name):
        file_data = api.drive.download(file_id)
        file_path = os.path.join(download_directory, file_name)
        with open(file_path, 'wb') as f:
            f.write(file_data)

    # Obtém a lista de arquivos do iCloud
    icloud_files = api.drive.get_list()

    # Baixa cada arquivo do iCloud
    for file in icloud_files:
        file_id = file['id']
        file_name = file['name']
        download_icloud_file(file_id, file_name)
        print(f"Arquivo '{file_name}' baixado com sucesso.")

    print("Todos os arquivos foram baixados.")

except Exception as e:
         print(e)