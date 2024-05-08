# Cocê pode usar a biblioteca google-api-python-client para interagir com a API do Google Drive e baixar os arquivos para o seu computador. 
# Antes de executar este script, você precisa obter credenciais de autenticação OAuth 2.0 para acessar a API do Google Drive.
# Aqui está um exemplo de como você pode fazer isso:

import os
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# Definir as permissões de escopo necessárias
SCOPES = ['https://www.googleapis.com/auth/drive.readonly']

def authenticate():
    creds = None
    # Verificar se existe um arquivo de token já armazenado
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json')
    # Se não houver credenciais válidas disponíveis, solicitar ao usuário que faça login
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Salvar as credenciais para uso futuro
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return creds

def download_files():
    # Autenticar
    creds = authenticate()
    service = build('drive', 'v3', credentials=creds)

    # Lista de arquivos na raiz do Google Drive
    results = service.files().list(
        pageSize=10, fields="nextPageToken, files(id, name)").execute()
    items = results.get('files', [])

    # Baixar cada arquivo encontrado
    if not items:
        print('Nenhum arquivo encontrado.')
    else:
        for item in items:
            file_id = item['id']
            file_name = item['name']
            request = service.files().get_media(fileId=file_id)
            fh = io.FileIO(file_name, 'wb')
            downloader = MediaIoBaseDownload(fh, request)
            done = False
            while done is False:
                status, done = downloader.next_chunk()
                print(f"Baixando {file_name}... {int(status.progress() * 100)}%")

if __name__ == '__main__':
    download_files()
