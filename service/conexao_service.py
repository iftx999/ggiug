from sqlalchemy.orm import Session
from models.conexao_model import Conexao
from schemas.conexao_schema import ConexaoCreate
from sqlalchemy import text


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

def listar_conexoes(db: Session):
    # Consulta direta na tabela unidadeoperacional
    sql = text("SELECT id, unidadeoperacional FROM unidadeoperacional")
    result = db.execute(sql).fetchall()

    # Debug
    print(f"Linhas retornadas: {len(result)}")
    for r in result:
        print(r)

    # Retorna lista de dicionários com id e nome
    return [{"id": r[0], "nome": r[1]} for r in result]