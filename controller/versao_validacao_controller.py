from fastapi import APIRouter, Depends, Path
from sqlalchemy.orm import Session
from database import get_db
from schemas.versao_validacao_schema import VersaoValidacaoCreate, VersaoValidacaoResponse
from service.versao_validacao_service import adicionar_versao_validacao

router = APIRouter(prefix="/versoes", tags=["Versões"])

@router.post("/{validacao_id}", response_model=VersaoValidacaoResponse)
def post_versao(validacao_id: int = Path(...), data: VersaoValidacaoCreate = None, db: Session = Depends(get_db)):
    return adicionar_versao_validacao(db, validacao_id, data)
