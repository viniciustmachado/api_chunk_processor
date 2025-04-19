import os
import requests
from dotenv import load_dotenv

# Carrega a chave da API do arquivo .env
load_dotenv()
api_key = os.getenv("ELEVENLABS_API_KEY")

# URL da API
url = "https://api.elevenlabs.io/v1/voices"

# Cabeçalhos com a chave da API
headers = {
    "xi-api-key": api_key
}

# Faz a requisição
response = requests.get(url, headers=headers)

# Verifica o status
if response.status_code == 200:
    data = response.json()
    print("\n🗣️ Suas vozes disponíveis:")
    for voice in data["voices"]:
        print(f"- Nome: {voice['name']}")
        print(f"  ID: {voice['voice_id']}\n")
else:
    print("❌ Erro ao obter vozes:", response.status_code)
    print(response.text)
