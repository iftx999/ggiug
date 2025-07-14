from pydantic import BaseModel
from typing import Optional

class ProjetoBase(BaseModel):
    nome: str
    descricao: Optional[str] = None  # corrigido indentação aqui

class ProjetoCreate(ProjetoBase):
    pass

class ProjetoResponse(ProjetoBase):
    id: int

    class Config:
        from_attributes = True  # substitui orm_mode no Pydantic v2
