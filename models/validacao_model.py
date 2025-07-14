from sqlalchemy import Column, Integer, String, Text, ForeignKey, Boolean, DateTime, func
from sqlalchemy.orm import relationship
from database import Base

class Validacao(Base):
    __tablename__ = "validacoes"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    descricao = Column(Text)
    ativo = Column(Boolean, default=True)

    projeto_id = Column(Integer, ForeignKey("projetos.id"), nullable=False)  # **Aqui está a chave estrangeira**

    projeto = relationship("Projeto", back_populates="validacoes")  # relacionamento inverso

    versoes = relationship("VersaoValidacao", back_populates="validacao")
