from sqlalchemy.orm import Session
from sqlalchemy.sql import text
from sqlalchemy import create_engine

from typing import List
from models.validacao_model import Validacao
from models.versao_validacao_model import VersaoValidacao
from models.conexao_model import Conexao
from fastapi import HTTPException
import sqlparse
from schemas.validacao_schema import ValidacaoCreate


def get_engine_by_conexao(conexao: Conexao):
    """
    Cria e retorna um SQLAlchemy engine baseado na url de conexão.
    Exemplo de url: "postgresql://user:password@host:port/dbname"
    """
    return create_engine(conexao.url_conexao)


def criar_validacao_com_versao(db: Session, data: ValidacaoCreate):
    nova_validacao = Validacao(
        nome=data.nome,
        descricao=data.descricao,
        projeto_id=data.projeto_id
    )
    db.add(nova_validacao)
    db.flush()  # para pegar o ID gerado

    versao = VersaoValidacao(
        validacao_id=nova_validacao.id,
        conexao_origem_id=data.versao.conexao_origem_id,
        conexao_destino_id=data.versao.conexao_destino_id,
        sql_origem=data.versao.sql_origem,
        sql_destino=data.versao.sql_destino
    )
    db.add(versao)
    db.commit()
    db.refresh(nova_validacao)
    return nova_validacao


def listar_validacoes_por_projeto(db: Session, projeto_id: int):
    return db.query(Validacao).filter(Validacao.projeto_id == projeto_id).all()


def buscar_validacao_por_id(db: Session, validacao_id: int):
    return db.query(Validacao).filter(Validacao.id == validacao_id).first()


def executar_validacao(validacao_id: int, db: Session):
    versao = (
        db.query(VersaoValidacao)
        .filter_by(validacao_id=validacao_id)
        .order_by(VersaoValidacao.id.desc())
        .first()
    )

    if not versao:
        raise Exception("Versão de validação não encontrada")

    conexao_origem = db.query(Conexao).get(versao.conexao_origem_id)
    conexao_destino = db.query(Conexao).get(versao.conexao_destino_id)

    if not conexao_origem or not conexao_destino:
        raise Exception("Conexão inválida")

    engine_origem = get_engine_by_conexao(conexao_origem)
    engine_destino = get_engine_by_conexao(conexao_destino)

    with engine_origem.connect() as conn_origem, engine_destino.connect() as conn_destino:
        result_origem = conn_origem.execute(text(versao.sql_origem)).fetchall()
        result_destino = conn_destino.execute(text(versao.sql_destino)).fetchall()

        iguais = result_origem == result_destino

        return {
            "resultado_origem": [dict(row._mapping) for row in result_origem],
            "resultado_destino": [dict(row._mapping) for row in result_destino],
            "iguais": iguais
        }


def executar_validacoes_somente_destino(validacao_ids: list[int], db: Session):
    resultados = []
    print("Entrou na função")

    for validacao_id in validacao_ids:
        versao = (
            db.query(VersaoValidacao)
            .filter_by(validacao_id=validacao_id)
            .order_by(VersaoValidacao.id.desc())
            .first()
        )

        if not versao:
            resultados.append({
                "validacao_id": validacao_id,
                "erro": "Versão de validação não encontrada"
            })
            continue

        conexao_destino = db.query(Conexao).get(versao.conexao_destino_id)

        if not conexao_destino:
            resultados.append({
                "validacao_id": validacao_id,
                "erro": "Conexão de destino inválida"
            })
            continue

        engine_destino = get_engine_by_conexao(conexao_destino)

        with engine_destino.connect() as conn_destino:
            result_destino = conn_destino.execute(text(versao.sql_destino)).fetchall()

            resultados.append({
                "validacao_id": validacao_id,
                "resultado_destino": [dict(row._mapping) for row in result_destino]
            })

    return resultados


 
def executar_sql_com_conexao(url_conexao: str, sql: str):
    sql_stripped = sql.strip().lower()
    parsed = sqlparse.parse(sql)
    statement = parsed[0]

    if statement.get_type() != "SELECT":
        raise HTTPException(status_code=400, detail="Apenas consultas SELECT são permitidas.")

    resultados = []
    try:
        engine = create_engine(url_conexao)
        with engine.connect() as conn:
            result = conn.execute(text(sql)).fetchall()
            resultados = [dict(row._mapping) for row in result]
        return {"resultado": resultados}
    except Exception as e:
        return {"erro": str(e)}
    

from sqlalchemy.orm import Session

def validar_fatura_por_ligacao(id_ligacao: int, id_conexao: int, db: Session):
    sql = text("SELECT f.id ,f.valor, f.datavencimento  FROM fatura f "
"join ligacao l on (l.id = f.idligacao ) "
"join medicaodetalhe mdt on (mdt.idligacao = l.id) "
"WHERE f.idligacao = :id_ligacao AND idfaturasituacao = 1 and mdt.retornadocoletor = 'S'")
    params = {"id_ligacao": id_ligacao}
    
    conexao = db.query(Conexao).filter_by(id=id_conexao).first()
    if not conexao:
        return {"erro": "Conexão não encontrada"}
    
    engine = get_engine_by_conexao(conexao)
    with engine.connect() as conn:
        resultado = conn.execute(sql, params).fetchall()
        return [dict(row._mapping) for row in resultado]

