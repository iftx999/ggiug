from sqlalchemy.orm import Session
from models.medicao_model import Medicao

from schemas.medicao_schema import MedicaoCreate

def criar_medicao(db: Session, medicao: MedicaoCreate):
    nova_medicao = Medicao(volmedido=medicao.volmedido)
    db.add(nova_medicao)
    db.commit()
    db.refresh(nova_medicao)
    return nova_medicao

def listar_medicoes(db: Session, id_ligacao: int, limit: int = 6):
    return (
        db.query(Medicao)
        .filter(Medicao.idligacao == id_ligacao, Medicao.retornadocoletor == 'S')
        .order_by(Medicao.id.desc())
        .limit(limit)
        .all()
    )
