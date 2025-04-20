# utils/auth.py

import os
from fastapi import Request, HTTPException
from fastapi.security.api_key import APIKeyHeader
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")
API_KEY_HEADER = APIKeyHeader(name="X-API-KEY", auto_error=False)

async def verificar_api_key(request: Request, api_key: str = None):
    """
    Middleware simples para verificar o header X-API-KEY em rotas protegidas.
    """
    if not api_key:
        api_key = request.headers.get("X-API-KEY")

    if api_key != API_KEY:
        raise HTTPException(status_code=403, detail="Chave de API inválida ou ausente.")
