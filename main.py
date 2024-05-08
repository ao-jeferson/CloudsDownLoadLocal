
import os
import sys
import click
import datetime
from pyicloud import PyiCloudService

# Diretório onde os arquivos serão salvos
download_directory = 'C:\\temp\\'
username ="jeferson.ao@icloud.com"
password = "slk350@K"


# Função para solicitar o código de verificação de dois fatores via SMS
def request_verification_code(api):
    api.send_verification_code()

# def icloud_login(username, password, sms_verification_callback):
#     datetime.datetime.now().strftime("%X %x %Z")
#     os.environ["TZ"] = "Brazil, America/Sao_Paulo"

#     api = PyiCloudService(username,password)

#     if api.requires_2fa:
#         print("Two-factor authentication required. Your trusted devices are:")

#         devices = api.trusted_devices
#         for i, device in enumerate(devices):
#             print(
#                 "  %s: %s"
#                 % (i, device.get("deviceName", "SMS to %s" % device.get("phoneNumber")))
#             )

#         device = click.prompt("Which device would you like to use?", default=0)
#         device = devices[device]
#         if not api.send_verification_code(device):
#             print("Failed to send verification code")
#             sys.exit(1)

#         code = click.prompt("Please enter validation code")
#         if not api.validate_verification_code(device, code):
#             print("Failed to verify verification code")
#             sys.exit(1)
#     return api


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
def download_icloud_files(folder_name, destination_path):
    api = icloud_login(username, password, request_verification_code)

    folder = api.drive[folder_name]
    for item in folder:
        if item.type == 'file':
            item.download(destination_path)


try:
    # Fazendo login
    api = icloud_login(username, password, request_verification_code)


    # # Obtém a lista de arquivos do iCloud
    icloud_files = api.drive.get_app_data() #  .drive.get_list()
    print("File Storage")
    print(icloud_files)

    for fl in icloud_files:
        print(str(fl['drivewsid']) +'\n')
        download_icloud_files(fl , download_directory)
         

    print("Arquivos baixados com sucesso!")
except Exception as e:
    print("Ocorreu um erro:", e)







# # Baixa cada arquivo do iCloud
# for file in icloud_files:
#     file_id = file['id']
#     file_name = file['name']
#     download_icloud_file(file_id, file_name)
#     print(f"Arquivo '{file_name}' baixado com sucesso.")

# print("Todos os arquivos foram baixados.")


# #
# # Devices
# #
# # print("Devices")
# # print(api.devices)
# # print(api.devices[0])
# # print(api.iphone)


# #
# # Location
# #
# # print("Location")
# # print(api.iphone.location())


# #
# # Status
# #
# # print("Status")
# # print(api.iphone.status())

# #
# # Play Sound
# #
# # api.iphone.play_sound()


# #
# # Events
# #
# # print("Events")
# # print(api.calendar.events())
# # from_dt = datetime.date(2018, 1, 1)
# # to_dt = datetime.date(2018, 1, 31)
# # print(api.calendar.events(from_dt, to_dt))


# # ========
# # Contacts
# # ========
# # print("Contacts")
# # for c in api.contacts.all():
# #     print(c.get("firstName"), c.get("phones"))


# # =======================
# # File Storage (Ubiquity)
# # =======================

# # You can access documents stored in your iCloud account by using the
# # ``files`` property's ``dir`` method:
# print("File Storage")
# print(api.files.dir())