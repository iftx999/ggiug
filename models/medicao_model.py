from sqlalchemy import Column, Integer, String
from database import Base

class Medicao(Base):
    __tablename__ = "medicaodetalhe"

    id = Column(Integer, primary_key=True, index=True)
    volmedido = Column(Integer, nullable=True)
    idligacao = Column(Integer, nullable=False)  # Adicione isso
    retornadocoletor = Column(String(1), nullable=True)  # 'S' ou 'N'