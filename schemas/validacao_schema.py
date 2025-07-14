from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class VersaoValidacaoCreate(BaseModel):
    sql_origem: Optional[str]
    sql_destino: Optional[str]

class ValidacaoCreate(BaseModel):
    nome: str
    descricao: Optional[str]
    versao: VersaoValidacaoCreate

class VersaoValidacaoResponse(BaseModel):
    id: int
    criado_em: datetime
    sql_origem: Optional[str]
    sql_destino: Optional[str]

    class Config:
        orm_mode = True

class ValidacaoResponse(BaseModel):
    id: int
    nome: str
    descricao: Optional[str]
    ativo: bool
    versoes: List[VersaoValidacaoResponse]

    class Config:
        orm_mode = True
