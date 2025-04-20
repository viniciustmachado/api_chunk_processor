# routers/processamento_router.py

import os
import uuid
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from fastapi.responses import PlainTextResponse

from services.processador import processar_arquivo, juntar_chunks
from utils.logger import get_logger
from utils.auth import verificar_api_key

router = APIRouter()
logger = get_logger()


@router.post(
    "/upload",
    summary="Envia um arquivo .txt para processamento com LLM",
    description="""
Este endpoint permite o envio de um arquivo `.txt` contendo uma transcrição (ex: aula, palestra, entrevista).

A API irá:
- Salvar o arquivo no servidor
- Dividir o conteúdo em partes (chunks)
- Enviar cada parte para o modelo OpenAI `gpt-4o`
- Processar e salvar o resultado de cada trecho individualmente

📌 Retorna um `arquivo_id` que deve ser usado para buscar o resultado final no endpoint `/resultado/{arquivo_id}`.
""",
    dependencies=[Depends(verificar_api_key)]
)
async def upload_arquivo(file: UploadFile = File(...)):
    if not file.filename.endswith(".txt"):
        raise HTTPException(status_code=400, detail="Apenas arquivos .txt são permitidos.")

    os.makedirs("storage/uploads", exist_ok=True)

    arquivo_id = str(uuid.uuid4())
    caminho = f"storage/uploads/{arquivo_id}.txt"

    with open(caminho, "wb") as f:
        f.write(await file.read())

    logger.info(f"📁 Arquivo salvo: {caminho}")

    processar_arquivo(caminho, arquivo_id)

    return {
        "arquivo_id": arquivo_id,
        "mensagem": "✅ Processamento iniciado com sucesso!"
    }


@router.get(
    "/resultado/{arquivo_id}",
    response_class=PlainTextResponse,
    summary="Retorna o texto completo processado e concatenado (formato Markdown)",
    description="""
Busca os resultados gerados para um `arquivo_id` previamente enviado via `/upload`.

A API:
- Lê todos os arquivos processados relacionados àquele ID
- Junta os textos em uma resposta única
- Retorna o conteúdo em **formato Markdown** (já pronto para publicação ou leitura)

Ideal para transformar transcrições longas em conteúdo legível e didático.
""",
    dependencies=[Depends(verificar_api_key)]
)
def obter_resultado(arquivo_id: str):
    try:
        texto_final = juntar_chunks(arquivo_id)
        return texto_final
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Arquivo não encontrado.")
    except Exception as e:
        logger.error(f"❌ Erro ao montar resultado: {e}")
        raise HTTPException(status_code=500, detail="Erro interno ao montar o resultado.")
