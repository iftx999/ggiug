from sqlalchemy import Column, Integer, Text, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from database import Base

class VersaoValidacao(Base):
    __tablename__ = "versoes_validacao"

    id = Column(Integer, primary_key=True, index=True)
    validacao_id = Column(Integer, ForeignKey("validacoes.id"))
    conexao_origem_id = Column(Integer, ForeignKey("conexoes.id"))
    conexao_destino_id = Column(Integer, ForeignKey("conexoes.id"))
    sql_origem = Column(Text)
    sql_destino = Column(Text)
    criado_em = Column(DateTime, server_default=func.now())

    validacao = relationship("Validacao", back_populates="versoes")
    conexao_origem = relationship("Conexao", back_populates="versoes_origem", foreign_keys=[conexao_origem_id])
    conexao_destino = relationship("Conexao", back_populates="versoes_destino", foreign_keys=[conexao_destino_id])
