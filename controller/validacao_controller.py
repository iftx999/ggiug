from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from database import get_db
from schemas.validacao_schema import ValidacaoCreate, ValidacaoResponse
from service.validacao_service import criar_validacao_com_versao, listar_validacoes_por_projeto, executar_validacoes_somente_destino, validar_fatura_por_ligacao

router = APIRouter(prefix="/validacoes", tags=["Validações"])

@router.post("/add", response_model=ValidacaoResponse)
def post_validacao(data: ValidacaoCreate, db: Session = Depends(get_db)):
    return criar_validacao_com_versao(db, data)

@router.get("/", response_model=list[ValidacaoResponse])
def get_validacoes(projeto_id: int = Query(...), db: Session = Depends(get_db)):
    return listar_validacoes_por_projeto(db, projeto_id)


@router.get("/executar/{validacao_id}")
def executar_validacao_endpoint(validacao_id: int, db: Session = Depends(get_db)):
    return executar_validacao(validacao_id, db)

@router.get("/executar-destino/{validacao_id}")
def testar_validacao_destino(validacao_id: int, db: Session = Depends(get_db)):
    return executar_validacoes_somente_destino([validacao_id], db)

@router.get("/validar-fatura/{id_ligacao}/{id_conexao}")
def validar_fatura(id_ligacao: int, id_conexao: int, db: Session = Depends(get_db)):
    return validar_fatura_por_ligacao(id_ligacao, id_conexao, db)

