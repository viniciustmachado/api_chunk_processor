import requests
import time

# URL base da API FastAPI
API_BASE_URL = "http://localhost:8000"

def enviar_arquivo_para_api(caminho_arquivo: str) -> str:
    """
    Envia um arquivo .txt para a API de processamento.
    Retorna o ID do arquivo processado.
    """
    url = f"{API_BASE_URL}/processar/upload"
    
    with open(caminho_arquivo, "rb") as f:
        files = {"file": (caminho_arquivo, f, "text/plain")}
        response = requests.post(url, files=files)

    if response.status_code == 200:
        return response.json()["arquivo_id"]
    else:
        raise Exception(f"Erro ao enviar arquivo: {response.status_code} - {response.text}")


def obter_texto_processado(arquivo_id: str) -> str:
    """
    Consulta o texto final processado com base no arquivo_id.
    Retorna o conteúdo em Markdown.
    """
    url = f"{API_BASE_URL}/processar/resultado/{arquivo_id}"
    response = requests.get(url)

    if response.status_code == 200:
        return response.text
    else:
        raise Exception(f"Erro ao obter resultado: {response.status_code} - {response.text}")


def processar_arquivo_local(caminho_arquivo: str, aguardar_resultado=True) -> str:
    arquivo_id = enviar_arquivo_para_api(caminho_arquivo)

    if not aguardar_resultado:
        return arquivo_id

    tempo_total = 0
    espera = 5

    while tempo_total <= 60:
        try:
            return obter_resultado_formatado(arquivo_id)
        except Exception:
            time.sleep(espera)
            tempo_total += espera

    raise TimeoutError("Arquivo não processado dentro do tempo esperado.")

    """
    Envia o arquivo e retorna o conteúdo final já processado.
    """
    arquivo_id = enviar_arquivo_para_api(caminho_arquivo)
    print(f"🆗 Arquivo enviado com ID: {arquivo_id}")

    print("⏳ Aguardando 5 segundos antes de buscar o resultado...")
    time.sleep(5)

    return obter_texto_processado(arquivo_id)

import requests

def obter_resultado_formatado(arquivo_id: str) -> str:
    """
    Busca o texto completo processado (em markdown) da API.
    """
    url = f"http://localhost:8000/processar/resultado/{arquivo_id}"
    response = requests.get(url)

    if response.status_code != 200:
        raise Exception(f"Erro ao obter resultado: {response.status_code} - {response.text}")

    return response.text
