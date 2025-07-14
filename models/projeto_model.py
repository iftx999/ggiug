from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship
from database import Base

class Projeto(Base):
    __tablename__ = "projetos"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, unique=True, nullable=False)
    descricao = Column(Text)

    conexoes = relationship("Conexao", back_populates="projeto", cascade="all, delete")
    validacoes = relationship("Validacao", back_populates="projeto", cascade="all, delete")
