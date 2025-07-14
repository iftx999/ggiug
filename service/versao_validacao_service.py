from sqlalchemy.orm import Session
from models.versao_validacao_model import VersaoValidacao
from schemas.versao_validacao_schema import VersaoValidacaoCreate

def adicionar_versao_validacao(db: Session, validacao_id: int, data: VersaoValidacaoCreate):
    nova = VersaoValidacao(
        validacao_id=validacao_id,
        conexao_origem_id=data.conexao_origem_id,
        conexao_destino_id=data.conexao_destino_id,
        sql_origem=data.sql_origem,
        sql_destino=data.sql_destino
    )
    db.add(nova)
    db.commit()
    db.refresh(nova)
    return nova
