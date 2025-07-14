from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class VersaoValidacaoBase(BaseModel):
    sql_origem: Optional[str]
    sql_destino: Optional[str]
    conexao_origem_id: int
    conexao_destino_id: int

class VersaoValidacaoCreate(VersaoValidacaoBase):
    pass

class VersaoValidacaoResponse(VersaoValidacaoBase):
    id: int
    criado_em: datetime

    class Config:
        orm_mode = True
