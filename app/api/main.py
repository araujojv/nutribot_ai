from fastapi import FastAPI  
from typing import List
from pydantic import BaseModel
from app.logic.metabolism import calcular_tmb, calcular_tdee
from app.nutrition.calculadora_alimento import calcular_refeicao

app = FastAPI()


class Usuario(BaseModel):
    peso: float
    altura: float
    idade: int
    sexo: str
    nivel_atividade: str

# Rota para calcular TMB e TDEE
@app.post("/calcular_gasto_energetico")
def calcular(usuario: Usuario):
    tmb = calcular_tmb(usuario.peso, usuario.altura, usuario.idade, usuario.sexo)
    tdee = calcular_tdee(tmb, usuario.nivel_atividade)
    return {
        "TMB": round(tmb, 2),
        "TDEE": round(tdee, 2)
    }


class ItemRefeicao(BaseModel):
    alimento: str
    gramas: float

@app.post("/calcular_refeicao")
def calcular(itens: List[ItemRefeicao]):
    return calcular_refeicao([item.dict() for item in itens])