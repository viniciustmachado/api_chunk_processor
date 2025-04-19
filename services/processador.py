# services/processador.py

import os
import openai
from dotenv import load_dotenv

# Carrega variáveis de ambiente do .env
load_dotenv()

# Define a chave da API OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")


def processar_arquivo(caminho_arquivo: str, arquivo_id: str):
    """
    Lê o arquivo .txt, divide em chunks e envia cada um para a OpenAI.
    Cada resposta é salva em um arquivo separado na pasta storage/processados/{arquivo_id}/.
    """
    with open(caminho_arquivo, "r", encoding="utf-8") as f:
        texto = f.read()

    # Divide o texto em pedaços de até 10.000 caracteres, com sobreposição de 400
    chunks = chunk_texto(texto, chunk_size=10000, overlap=400)

    # Cria a pasta de saída se não existir
    pasta_saida = f"storage/processados/{arquivo_id}"
    os.makedirs(pasta_saida, exist_ok=True)

    for i, chunk in enumerate(chunks):
        prompt = montar_prompt(chunk)

        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.0
        )

        texto_processado = response.choices[0].message["content"].strip()

        # Salva cada resposta da OpenAI como um .txt separado
        nome_arquivo = f"{str(i+1).zfill(2)}.txt"
        caminho_saida = os.path.join(pasta_saida, nome_arquivo)

        with open(caminho_saida, "w", encoding="utf-8") as out:
            out.write(texto_processado)


def montar_prompt(chunk: str) -> str:
    """
    Lê o conteúdo de prompt_texto.txt e anexa o chunk de texto ao final.
    Garante o caminho absoluto da raiz do projeto.
    """
    raiz_projeto = os.path.dirname(os.path.dirname(__file__))
    caminho_prompt = os.path.join(raiz_projeto, "prompt_texto.txt")

    try:
        with open(caminho_prompt, "r", encoding="utf-8") as f:
            prompt_base = f.read().strip()
    except FileNotFoundError:
        prompt_base = "Corrija e formate o texto abaixo:"

    return f"{prompt_base}\n\n{chunk}"


def chunk_texto(texto: str, chunk_size=10000, overlap=400):
    """
    Divide o texto em pedaços menores para envio à OpenAI.
    """
    return [
        texto[i:i + chunk_size]
        for i in range(0, len(texto), chunk_size - overlap)
    ]


def juntar_chunks(arquivo_id: str) -> str:
    """
    Junta todos os arquivos .txt de chunks processados em um único texto markdown.
    """
    pasta = f"storage/processados/{arquivo_id}"

    if not os.path.exists(pasta):
        raise FileNotFoundError("Pasta de chunks não encontrada.")

    arquivos = sorted(os.listdir(pasta))  # Garante ordem de leitura correta

    texto_final = ""

    for nome in arquivos:
        caminho = os.path.join(pasta, nome)
        with open(caminho, "r", encoding="utf-8") as f:
            texto_final += f.read().strip() + "\n\n"

    return texto_final.strip()
