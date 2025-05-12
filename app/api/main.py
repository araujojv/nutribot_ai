from fastapi import FastAPI  
from typing import List
from pydantic import BaseModel
from app.logic.metabolism import calcular_tmb, calcular_tdee
from app.models.refeicao import Refeicao
from app.nutrition.calculadora_alimento import calcular_refeicao
from sqlalchemy.orm import Session
from fastapi import Depends
from app.database import SessionLocal
from typing import List
app = FastAPI()


class Usuario(BaseModel):
    peso: float
    altura: float
    idade: int
    sexo: str
    nivel_atividade: str
    objetivo: str # emagrecer, manter, ganhar 

# Rota para calcular TMB e TDEE
@app.post("/calcular_gasto_energetico")
def calcular(usuario: Usuario):
    tmb = calcular_tmb(usuario.peso, usuario.altura, usuario.idade, usuario.sexo)
    tdee = calcular_tdee(tmb, usuario.nivel_atividade)
    objetivo = usuario.objetivo.lower()
    if objetivo == "emagrecer":
        meta = tdee - 500
    elif objetivo == "ganhar":
        meta = tdee + 500 
    else: #manter 
        meta = tdee
    
    
    return {
        "TMB": round(tmb, 2),
        "TDEE": round(tdee, 2),
        "meta_calorica_diaria": round(meta, 2),
        "objetivo": objetivo
    }


class ItemRefeicao(BaseModel):
    alimento: str
    gramas: float

@app.post("/calcular_refeicao")
def calcular(itens: List[ItemRefeicao]):
    return calcular_refeicao([item.dict() for item in itens])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/refeicao")
def listar_refeicoes(db: Session = Depends(get_db)):
    refeicoes = db.query(Refeicao).order_by(Refeicao.horario.desc()).all()
    return [
        {
            "id": r.id,
            "alimento": r.alimento,
            "gramas": r.gramas,
            "calorias": r.calorias,
            "proteinas": r.proteinas,
            "carboidratos": r.carboidratos,
            "gorduras": r.gorduras,
            "horario": r.horario
        }
        for r in refeicoes
    ]
    
    
