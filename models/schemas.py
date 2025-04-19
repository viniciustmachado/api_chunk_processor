# models/schemas.py

from pydantic import BaseModel


class ResultadoProcessamento(BaseModel):
    """
    Modelo de saída alternativo, caso você queira retornar o texto final como JSON.
    (Atualmente estamos usando texto puro com PlainTextResponse.)
    """
    arquivo_id: str
    resultado: str
