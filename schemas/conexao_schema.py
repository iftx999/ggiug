from pydantic import BaseModel
from typing import Optional

class ConexaoBase(BaseModel):
    nome: str
    tipo: str  # origem ou destino
    url_conexao: str

class ConexaoCreate(ConexaoBase):
    projeto_id: int

class ConexaoResponse(ConexaoBase):
    id: int
    projeto_id: int

    class Config:
        orm_mode = True
