from sqlalchemy.orm import Session
from models.conexao_model import Conexao
from schemas.conexao_schema import ConexaoCreate

def criar_conexao(db: Session, conexao: ConexaoCreate):
    nova = Conexao(**conexao.dict())
    db.add(nova)
    db.commit()
    db.refresh(nova)
    return nova

def listar_conexoes_por_projeto(db: Session, projeto_id: int):
    return db.query(Conexao).filter(Conexao.projeto_id == projeto_id).all()

def buscar_conexao_por_id(db: Session, conexao_id: int):
    return db.query(Conexao).filter(Conexao.id == conexao_id).first()

import logging
from sqlalchemy.orm import Session
from sqlalchemy import text

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

def listar_conexoes(db: Session):
    # SQL puro para pegar tudo da tabela unidadeoperacional
    sql = text("SELECT * FROM unidadeoperacional ")
    result = db.execute(sql).fetchall()
    
    # Debug: mostra o que veio do banco
    print("RESULTADOS:", result)
    
    # Retorna como lista de dicionários
    return [{"id": r[0], "unidadeoperacional": r[1]} for r in result]
