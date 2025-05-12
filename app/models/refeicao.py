from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
Base = declarative_base()

class Refeicao(Base):
    __tablename__ = "refeicoes"

    id = Column(Integer, primary_key=True, index=True)
    alimento = Column(String)
    gramas = Column(Float)
    calorias = Column(Float)
    proteinas = Column(Float)
    carboidratos = Column(Float)
    gorduras = Column(Float)
    horario = Column(DateTime, default=datetime.utcnow)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"))
    usuario = relationship("Usuario", backref="refeicoes")