from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from database import get_db
from service.medicao_service import criar_medicao, listar_medicoes
from schemas.medicao_schema import MedicaoCreate, MedicaoResponse
from typing import List

router = APIRouter(prefix="/medicoes", tags=["Medições"])

@router.post("/", response_model=MedicaoResponse)
def criar(medicao: MedicaoCreate, db: Session = Depends(get_db)):
    return criar_medicao(db, medicao)

@router.get("/", response_model=List[MedicaoResponse])
def listar(id_ligacao: int = Query(..., description="ID da ligação"), db: Session = Depends(get_db)):
    """
    Lista as últimas 6 medições de uma ligação específica que retornaram do coletor.
    """
    return listar_medicoes(db, id_ligacao=id_ligacao)