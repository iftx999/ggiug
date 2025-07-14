from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db  # importa o nome correto da dependência
from typing import List
from sqlalchemy.ext.asyncio import create_async_engine
from models.conexao_model import Conexao
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from fastapi import APIRouter, Depends, Query, HTTPException

import logging
import traceback

from schemas.validacao_schema import ValidacaoCreate, ValidacaoResponse
from service.validacao_service import (
    criar_validacao_com_versao,
    listar_validacoes_por_projeto,
    executar_validacao,
    executar_validacoes_somente_destino
  
)

router = APIRouter(prefix="/validacoes", tags=["Validações"])

def get_async_engine_by_conexao(conexao: Conexao):
    return create_async_engine(conexao.url_conexao, echo=True, future=True)

@router.post("/add", response_model=ValidacaoResponse)
def post_validacao(data: ValidacaoCreate, db: Session = Depends(get_db)):
    """
    Cria uma nova validação com versão associada.
    """
    try:
        return criar_validacao_com_versao(db, data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=list[ValidacaoResponse])
def get_validacoes(projeto_id: int = Query(..., description="ID do projeto"), db: Session = Depends(get_db)):
    """
    Lista todas as validações de um projeto específico.
    """
    try:
        validacoes = listar_validacoes_por_projeto(db, projeto_id)
        return validacoes
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/executar/{validacao_id}")
def executar_validacao_endpoint(validacao_id: int, db: Session = Depends(get_db)):
    """
    Executa uma validação comparando origem e destino.
    """
    try:
        resultado = executar_validacao(validacao_id, db)
        return resultado
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


from fastapi import Query

@router.get("/executar-destino")
async def executar_validacoes_endpoint(
    validacao_ids: list[int] = Query(...),
    db: AsyncSession = Depends(get_db)
):
    try:
        resultados = await executar_validacoes_somente_destino(validacao_ids, db)
        return resultados
    except Exception:
        import logging, traceback
        logging.error("Erro executando validações:\n" + traceback.format_exc())
        raise HTTPException(status_code=400, detail="Erro interno ao executar validações")

        