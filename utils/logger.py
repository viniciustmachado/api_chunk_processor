# utils/logger.py

import logging
import os
import requests
from dotenv import load_dotenv

# Carrega variáveis de ambiente do arquivo .env
load_dotenv()

# Configurações da ElevenLabs
ELEVEN_API_KEY = os.getenv("ELEVENLABS_API_KEY")
ELEVEN_VOICE_ID = os.getenv("ELEVENLABS_VOICE_ID", "33B4UnXyTNbgLmdEDh5P")  # fallback
ELEVEN_MODEL_ID = os.getenv("ELEVENLABS_MODEL_ID", "eleven_multilingual_v2")  # fallback seguro

def get_logger():
    """
    Cria e configura um logger para mostrar mensagens no terminal.
    Nível: INFO (exibe informações e erros).
    """
    logging.basicConfig(
        level=logging.INFO,
        format="[%(levelname)s] %(asctime)s - %(message)s"
    )
    return logging.getLogger("api_chunk_processor")


def primeiros_caracteres_sem_cortar(texto: str, limite: int = 400) -> str:
    """
    Retorna os primeiros 'limite' caracteres do texto, sem cortar a última palavra.
    """
    if len(texto) <= limite:
        return texto

    corte = texto[:limite]
    if texto[limite] != " ":
        corte = corte.rsplit(" ", 1)[0]
    return corte.strip()


def gerar_audio_elevenlabs(texto: str, nome_arquivo: str = "saida.mp3") -> str:
    """
    Gera um áudio com a ElevenLabs a partir do texto fornecido.
    Salva como .mp3 na pasta storage/public e retorna o caminho completo.
    """
    if not ELEVEN_API_KEY:
        raise ValueError("API Key da ElevenLabs não encontrada no .env")

    url = f"https://api.elevenlabs.io/v1/text-to-speech/{ELEVEN_VOICE_ID}"
    headers = {
        "xi-api-key": ELEVEN_API_KEY,
        "Content-Type": "application/json"
    }
    body = {
        "text": texto,
        "model_id": ELEVEN_MODEL_ID,
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.75
        }
    }

    response = requests.post(url, headers=headers, json=body)

    if response.status_code == 200:
        os.makedirs("storage/public", exist_ok=True)
        caminho = os.path.join("storage/public", nome_arquivo)
        with open(caminho, "wb") as f:
            f.write(response.content)
        return caminho
    else:
        raise Exception(f"Erro na ElevenLabs: {response.status_code} - {response.text}")
