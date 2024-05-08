from onedrivesdk import AuthProvider, Client
from onedrivesdk.helpers import GetAuthCodeServer

def authenticate():
    redirect_uri = 'http://localhost:8080/'
    client_id = 'seu_client_id'
    client_secret = 'seu_client_secret'
    scopes = ['wl.signin', 'wl.offline_access', 'onedrive.readwrite']

    client = Client(None, None, None)
    auth_provider = AuthProvider(client_id, scopes)
    auth_url = auth_provider.get_auth_url(redirect_uri)

    code = GetAuthCodeServer.get_auth_code(auth_url, redirect_uri)
    auth_provider.authenticate(code, redirect_uri, client_secret)
    client.auth_provider = auth_provider
    return client

def download_files(client):
    items = client.item(drive='me', id='root').children.get()
    for item in items:
        if item.folder is None:
            print("Downloading:", item.name)
            with open(item.name, "wb") as f:
                client.item(drive='me', id=item.id).download(f)

if __name__ == '__main__':
    client = authenticate()
    download_files(client)
