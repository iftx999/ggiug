from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from schemas.projeto_schema import ProjetoCreate, ProjetoResponse
from service.projeto_service import criar_projeto, listar_projetos

router = APIRouter(prefix="/projetos", tags=["Projetos"])

@router.post("/add")
def criar_projeto_endpoint(projeto: ProjetoCreate, db: Session = Depends(get_db)):
    return criar_projeto(db, projeto)  # chama a função do service

@router.get("/", response_model=list[ProjetoResponse])
def get_projetos(db: Session = Depends(get_db)):
    return listar_projetos(db)
