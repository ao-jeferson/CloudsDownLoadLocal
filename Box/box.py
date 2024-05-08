from boxsdk import OAuth2, Client

# Configurações de autenticação
CLIENT_ID = 'sua_client_id'
CLIENT_SECRET = 'seu_client_secret'
ACCESS_TOKEN = 'seu_access_token'  # Você pode obtê-lo manualmente uma vez e reutilizá-lo, ou pode autenticar o usuário

# Configuração da autenticação
oauth2 = OAuth2(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    access_token=ACCESS_TOKEN,
)

# Criação do cliente
client = Client(oauth2)

# Obtendo o usuário
user = client.user(user_id='me').get()

# Obtendo todos os arquivos e pastas do usuário
items = client.folder(folder_id='0').get_items()

# Baixando todos os arquivos
for item in items:
    if isinstance(item, client.file_class):
        file_path = '/caminho/para/salvar/' + item.name
        with open(file_path, 'wb') as f:
            client.file(file_id=item.id).download_to(f)
            print(f'Arquivo "{item.name}" baixado com sucesso para {file_path}')
