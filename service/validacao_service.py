from sqlalchemy.orm import Session
from sqlalchemy.sql import text
from sqlalchemy import create_engine

import logging
import traceback

from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text

from sqlalchemy import bindparam

from sqlalchemy import text, bindparam
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from typing import List
from models.validacao_model import Validacao
from models.versao_validacao_model import VersaoValidacao
from models.conexao_model import Conexao
from schemas.validacao_schema import ValidacaoCreate
from database import get_db


from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy import text, select
from sqlalchemy.future import select

def get_async_engine_by_conexao(conexao: Conexao):
    return create_async_engine(conexao.url_conexao, echo=True, future=True)


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




async def executar_validacoes_somente_destino(validacao_ids: list[int], db: AsyncSession):
    resultados = []

    # Query para pegar versões usando IN com expanding=True
    query = text(
        "SELECT * FROM versoes_validacao WHERE validacao_id IN :vids ORDER BY id DESC"
    ).bindparams(bindparam("vids", expanding=True))

    result = await db.execute(query, {"vids": validacao_ids})
    versoes = result.fetchall()

    # Indexa a versão mais recente por validacao_id
    versoes_por_id = {}
    for versao in versoes:
        vid = versao._mapping["validacao_id"]
        if vid not in versoes_por_id:
            versoes_por_id[vid] = versao

    for validacao_id in validacao_ids:
        versao = versoes_por_id.get(validacao_id)
        if not versao:
            resultados.append({
                "validacao_id": validacao_id,
                "erro": "Versão de validação não encontrada"
            })
            continue

        conexao_destino = await db.get(Conexao, versao._mapping["conexao_destino_id"])
        if not conexao_destino:
            resultados.append({
                "validacao_id": validacao_id,
                "erro": "Conexão de destino inválida"
            })
            continue

        # Verifica se URL do destino tem driver asyncpg
        if "asyncpg" not in conexao_destino.url_conexao:
            resultados.append({
                "validacao_id": validacao_id,
                "erro": f"URL da conexão destino não está usando driver asyncpg: {conexao_destino.url_conexao}"
            })
            continue

        engine_destino = create_async_engine(conexao_destino.url_conexao, future=True)
        async with engine_destino.connect() as conn_destino:
            result_destino = await conn_destino.execute(text(versao._mapping["sql_destino"]))
            rows = result_destino.fetchall()  # SEM await aqui
            resultados.append({
                "validacao_id": validacao_id,
                "resultado_destino": [dict(row._mapping) for row in rows]
            })

    return resultados