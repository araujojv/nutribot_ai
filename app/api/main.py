from fastapi import FastAPI  
from pydantic import BaseModel
from app.logic.metabolism import calcular_tmb, calcular_tdee

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
