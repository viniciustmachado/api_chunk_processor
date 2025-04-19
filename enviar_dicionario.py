import os
import requests
from dotenv import load_dotenv

load_dotenv()

# Defina sua chave de API e o caminho para o arquivo .pls
api_key = os.getenv("ELEVENLABS_API_KEY")
file_path = os.path.abspath("dictionary.pls")

# Endpoint da API
url = "https://api.elevenlabs.io/v1/pronunciation-dictionaries/add-from-file"

# Cabeçalhos da requisição
headers = {
    "xi-api-key": api_key
}

# Dados do formulário
data = {
    "name": "dictionary",
    "description": "Descrição do dicionário"
}

# Arquivo a ser enviado
with open(file_path, "rb") as f:
    files = {
        "file": ("dictionary.pls", f, "application/pls+xml")
    }
    response = requests.post(url, headers=headers, data=data, files=files)

# Verifica a resposta
if response.status_code == 200:
    dict_result = response.json()
    print("Dicionário carregado com sucesso!")
    print("ID do dicionário:", dict_result["id"])
    print("ID da versão:", dict_result["version_id"])
else:
    print("Erro ao carregar o dicionário:")
    print("Status Code:", response.status_code)
    print("Resposta:", response.text)
