# routers/audio_router.py

import os
import uuid
from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from fastapi.responses import HTMLResponse

from services.processador import processar_arquivo, juntar_chunks
from utils.logger import (
    get_logger,
    primeiros_caracteres_sem_cortar,
    gerar_audio_elevenlabs,
)

router = APIRouter()
logger = get_logger()


@router.post(
    "/audio",
    summary="Processa e retorna áudio e texto (pt-BR)",
    description="""
Envia um arquivo `.txt` com transcrição. A API processa com a OpenAI (gpt-4o), extrai os primeiros 400 caracteres e gera um áudio com a ElevenLabs (pt-BR).

Retorna:
- Link para o áudio (.mp3)
- Link para o texto processado (.txt)
"""
)



async def upload_gerar_audio(file: UploadFile = File(...)):
    """
    Processa um arquivo .txt com a OpenAI e gera:
    - Um áudio com os primeiros 400 caracteres (sem cortar palavras)
    - Um .txt com o conteúdo final completo pós-processamento
    Retorna links para download.
    """
    if not file.filename.endswith(".txt"):
        raise HTTPException(status_code=400, detail="Apenas arquivos .txt são permitidos.")

    os.makedirs("storage/uploads", exist_ok=True)
    os.makedirs("storage/public", exist_ok=True)

    # Gera identificador único
    arquivo_id = str(uuid.uuid4())
    caminho_entrada = f"storage/uploads/{arquivo_id}.txt"
    caminho_txt_saida = f"storage/public/{arquivo_id}.txt"
    caminho_mp3_saida = f"storage/public/{arquivo_id}.mp3"

    # Salva o arquivo enviado
    with open(caminho_entrada, "wb") as f:
        f.write(await file.read())

    logger.info(f"📁 Arquivo salvo: {caminho_entrada}")

    # Processamento
    processar_arquivo(caminho_entrada, arquivo_id)

    try:
        texto_final = juntar_chunks(arquivo_id)

        # Salva o texto final como .txt
        with open(caminho_txt_saida, "w", encoding="utf-8") as f:
            f.write(texto_final)

        # Gera trecho para áudio
        trecho = primeiros_caracteres_sem_cortar(texto_final, limite=400)
        gerar_audio_elevenlabs(trecho, nome_arquivo=f"{arquivo_id}.mp3")

    except Exception as e:
        logger.error(f"❌ Erro ao processar ou gerar arquivos: {e}")
        raise HTTPException(status_code=500, detail="Erro interno durante o processamento.")

    # Retorna URLs dos arquivos gerados
    return JSONResponse(
        content={
            "audio_url": f"/media/{arquivo_id}.mp3",
            "texto_url": f"/media/{arquivo_id}.txt"
        }
    )







@router.get("/listar-arquivos", response_class=HTMLResponse, summary="Painel HTML com os arquivos gerados")
def listar_arquivos():
    """
    Gera um painel simples em HTML listando todos os .mp3 e .txt disponíveis na pasta pública.
    """
    pasta_publica = "storage/public"

    if not os.path.exists(pasta_publica):
        return "<h3>⚠️ Nenhum arquivo encontrado.</h3>"

    arquivos = sorted(os.listdir(pasta_publica))
    if not arquivos:
        return "<h3>⚠️ Nenhum arquivo encontrado.</h3>"

    html = "<h2>📂 Arquivos disponíveis para download:</h2><ul>"
    for nome in arquivos:
        link = f"/media/{nome}"
        html += f'<li><a href="{link}" target="_blank">{nome}</a></li>'
    html += "</ul>"

    return html
