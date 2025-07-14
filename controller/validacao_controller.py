from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.conexao_model import Conexao
from schemas.validacao_schema import ValidacaoCreate, ValidacaoResponse
from service.validacao_service import (
    criar_validacao_com_versao,
    listar_validacoes_por_projeto,
    executar_validacao,
    executar_validacao_somente_destino,
)

router = APIRouter(prefix="/validacoes", tags=["Validações"])

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

@router.get("/executar-destino/{validacao_id}")
def executar_validacao_somente_endpoint(validacao_id: int, db: Session = Depends(get_db)):
    """
    Executa validação apenas no destino.
    """
    try:
        resultado = executar_validacao_somente_destino(validacao_id, db)
        return resultado
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))