# main.py

from fastapi import FastAPI
from routers import processamento_router, audio_router
from fastapi.staticfiles import StaticFiles

# Instância da aplicação FastAPI
app = FastAPI(
    title="🧠 API de Transcrição Inteligente",
    description="""
    
🚀 Destaque para o endpoint PROCESSAR/AUDIO, que é a função principal desta API 🚀    

API que recebe arquivos de transcrição (.txt), divide em partes, envia para o modelo gpt-4o da OpenAI para revisão didática e retorna:

✅ Texto final (.txt)  
🔊 Áudio gerado com ElevenLabs (pt-BR) — (Primeiros 400 caracteres para exemplo)

Ideal para transformar transcrições em conteúdo acessível.
""",
    version="1.0.0"
)

# Rota principal para evitar tela branca no navegador
@app.get("/")
def raiz():
    return {"mensagem": "🚀 API ativa! Acesse /docs para explorar."}

# Rotas da aplicação
app.include_router(processamento_router.router, prefix="/processar")
app.include_router(audio_router.router, prefix="/processar")

# Expor arquivos públicos via /media
app.mount("/media", StaticFiles(directory="storage/public"), name="media")
