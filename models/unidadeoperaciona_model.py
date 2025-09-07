from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from database import Base

class UnidadeOperacional(Base):
    __tablename__ = "unidadeoperacional"

    id = Column(Integer, primary_key=True, index=True)
    unidadeoperacional = Column(String, nullable=False)

  