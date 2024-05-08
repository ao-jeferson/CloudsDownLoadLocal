import os
import requests
from bs4 import BeautifulSoup

# Insira suas credenciais do iCloud Drive aqui
apple_id = "jeferson.ao@icloud.com"
password = "slk350@K"

# URL base do iCloud Drive (pode variar de acordo com a região)
url_base = "https://www.icloud.com/iclouddrive/"

# Pasta local para salvar os arquivos baixados
pasta_local = "C:/temp/"  # Altere para o diretório desejado
