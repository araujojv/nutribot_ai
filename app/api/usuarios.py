from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.usuario import Usuario as UsuarioModel
from app.auth import hash_senha
from pydantic import BaseModel

router = APIRouter()

# Esquema de entrada de dados
class UsuarioCreate(BaseModel):
    nome: str
    email: str
    senha: str

@router.post("/usuarios")
def criar_usuario(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    # Verifica se email já existe
    if db.query(UsuarioModel).filter(UsuarioModel.email == usuario.email).first():
        raise HTTPException(status_code=400, detail="Email já está em uso")

    usuario_novo = UsuarioModel(
        nome=usuario.nome,
        email=usuario.email,
        senha=hash_senha(usuario.senha)
    )
    db.add(usuario_novo)
    db.commit()
    db.refresh(usuario_novo)
    return {"id": usuario_novo.id, "email": usuario_novo.email, "nome": usuario_novo.nome}
