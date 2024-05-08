import os
from pyicloud import PyiCloudService

# Configurações
USERNAME = "jeferson.ao@icloud.com"
PASSWORD = "slk350@K"
DESTINATION_PATH = 'C:\\Temp\\'

def download_files(api, folder, destination_path):
    for item in folder:
        if item["type"] == "FOLDER":
            folder_path = os.path.join(destination_path, item["name"])
            os.makedirs(folder_path, exist_ok=True)
            download_files(api, api.drive[item["id"]]["items"], folder_path)
        elif item["type"] == "FILE":
            file_path = os.path.join(destination_path, item["name"])
            api #(item["name"]+'.'+['extension'],file_path)

def download_icloud_files(username, password, destination_path):
    api = PyiCloudService(username, password)

    if api.requires_2fa:
        code = input("Enter the code you received of your second authentication factor: ")
        api = PyiCloudService(username, password, code)

    root_folder = api.drive.root
    download_files(api, root_folder.data['items'] , destination_path)

if __name__ == "__main__":
    download_icloud_files(USERNAME, PASSWORD, DESTINATION_PATH)
