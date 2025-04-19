import os
import requests
from dotenv import load_dotenv

#  Caminho absoluto do .env na raiz do projeto
raiz_projeto = os.path.dirname(os.path.dirname(__file__))  # sobe um nível
caminho_env = os.path.join(raiz_projeto, ".env")

print("🔧 Carregando variáveis de ambiente...")
load_dotenv(dotenv_path=caminho_env)

# Carrega a chave da API do arquivo .env ou define diretamente
api_key = os.getenv("ELEVENLABS_API_KEY")  # Certifique-se de que a variável de ambiente está definida
if not api_key:
    raise ValueError(" API KEY da ElevenLabs não encontrada no .env!")

# ❌ --------- BLOCO COMENTADO: Upload de dicionário fonético ---------
# # Caminho para o arquivo .pls
# caminho_dict = "C:\\Users\\DELL\\Documents\\GitHub\\api_chunk_processor\\audio\\dictionary.pls"

# # Endpoint da API para adicionar o dicionário
# url = "https://api.elevenlabs.io/v1/pronunciation-dictionaries/add-from-file"

# # Cabeçalhos da requisição
# headers = {
#     "xi-api-key": api_key
# }

# # Dados do formulário
# data = {
#     "name": "dictionary",
#     "description": "Dicionário fonético para termos relacionados ao autismo"
# }

# # Arquivo a ser enviado
# with open(caminho_dict, "rb") as f:
#     files = {
#         "file": ("dictionary.pls", f, "application/pls+xml")
#     }
#     response = requests.post(url, headers=headers, data=data, files=files)

# # Verifica a resposta
# if response.status_code == 200:
#     dict_result = response.json()
#     print("✅ Dicionário carregado com sucesso!")
#     print("ID do dicionário:", dict_result["id"])
#     print("ID da versão:", dict_result["version_id"])
# else:
#     print("❌ Erro ao carregar o dicionário:")
#     print("Status Code:", response.status_code)
#     print("Resposta:", response.text)
# 📴 -------------------------------------------------------------------
