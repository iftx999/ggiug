from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from database import get_db
from schemas.conexao_schema import ConexaoCreate, ConexaoResponse
from service.conexao_service import criar_conexao, listar_conexoes_por_projeto, listar_conexoes
from models.conexao_model import Conexao

router = APIRouter(prefix="/conexoes", tags=["Conexões"])

@router.post("/salvar", response_model=ConexaoResponse)
def post_conexao(conexao: ConexaoCreate, db: Session = Depends(get_db)):
    return criar_conexao(db, conexao)

@router.get("/", response_model=list[ConexaoResponse])
def get_conexoes(projeto_id: int = Query(...), db: Session = Depends(get_db)):
    return listar_conexoes_por_projeto(db, projeto_id)

@router.get("/list")
def listar_conexoes_endpoint(db: Session = Depends(get_db)):
    # Chama o método do service que retorna unidadeoperacional
    return listar_conexoes(db)