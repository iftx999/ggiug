from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Conexao(Base):
    __tablename__ = "conexoes"

    id = Column(Integer, primary_key=True, index=True)
    projeto_id = Column(Integer, ForeignKey("projetos.id"))
    nome = Column(String, nullable=False)
    tipo = Column(String, nullable=False)  # origem | destino
    url_conexao = Column(Text, nullable=False)

    projeto = relationship("Projeto", back_populates="conexoes")
    versoes_origem = relationship("VersaoValidacao", back_populates="conexao_origem", foreign_keys="VersaoValidacao.conexao_origem_id")
    versoes_destino = relationship("VersaoValidacao", back_populates="conexao_destino", foreign_keys="VersaoValidacao.conexao_destino_id")
