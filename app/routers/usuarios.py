from fastapi import APIRouter, Depends, HTTPException, status
from app import schemas, crud_db
from typing import List
from sqlalchemy.orm import Session
from app.database_connection import get_db

router = APIRouter(
    prefix="/usuarios",
    tags=["Usuarios"],
    responses={status.HTTP_404_NOT_FOUND: {"message": "No encontrado"}}
)

@router.post("/", response_model=schemas.UsuarioOut)
def crear_usuario(usuario: schemas.UsuarioCreate, db: Session = Depends(get_db)):
    db_user = crud_db.crear_usuario(db, usuario)
    if not db_user:
        raise HTTPException(status_code=400, detail="Este usuario ya ha sido registrado")
    return db_user

@router.get("/{user_id}", response_model=schemas.UsuarioOut)
def obtener_usuario(user_id: int, db: Session = Depends(get_db)):
    usuario = crud_db.obtener_usuario(db, user_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario

@router.get("/", response_model=List[schemas.UsuarioOut])
def obtener_todos_usuarios(db: Session = Depends(get_db)):
    return crud_db.obtener_todos_usuarios(db)

@router.put("/{user_id}", response_model=schemas.UsuarioOut)
def actualizar_usuario(user_id: int, usuario: schemas.UsuarioUpdate, db: Session = Depends(get_db)):
    db_usuario = crud_db.actualizar_usuario(db, user_id, usuario)
    if not db_usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return db_usuario

@router.delete("/{user_id}")
def eliminar_usuario(user_id: int, db: Session = Depends(get_db)):
    db_usuario = crud_db.eliminar_usuario(db, user_id)
    if not db_usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return {"message": "Usuario eliminado"}