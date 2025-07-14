from sqlalchemy.orm import Session
from models.projeto_model import Projeto
from schemas.projeto_schema import ProjetoCreate

def criar_projeto(db: Session, projeto: ProjetoCreate):
    novo = Projeto(**projeto.dict())
    db.add(novo)
    db.commit()
    db.refresh(novo)
    return novo

def listar_projetos(db: Session):
    return db.query(Projeto).all()

def buscar_projeto_por_id(db: Session, projeto_id: int):
    return db.query(Projeto).filter(Projeto.id == projeto_id).first()
