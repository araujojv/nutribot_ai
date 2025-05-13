from sqlalchemy import Column, Integer, String
from . import Base
from sqlalchemy.orm import relationship
class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    email = Column(String, unique=True, index=True)
    senha = Column(String, nullable=False)
