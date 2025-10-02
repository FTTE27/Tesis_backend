from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlalchemy.orm import Session
from app import schemas, crud_db
from app.database_connection import get_db
from app.routers.auth_users import usuario_opcional
import base64


router = APIRouter(
    prefix="/registros",
    tags=["Registros"],
    responses={status.HTTP_404_NOT_FOUND: {"message": "No encontrado"}}
)


@router.post("/", response_model=schemas.RegistroOut)
def crear_registro(
    registro: schemas.RegistroCreate,
    db: Session = Depends(get_db),
    current_user: schemas.UsuarioOut = Depends(usuario_opcional)
):
    # Si no hay usuario → Guest
    username = current_user.username if current_user else "Guest"
    return crud_db.crear_registro(db, registro, username)


@router.get("/{registro_id}", response_model=schemas.RegistroOut)
def obtener_registro(registro_id: int, db: Session = Depends(get_db)):
    registro = crud_db.obtener_registro(db, registro_id)
    if not registro:
        raise HTTPException(status_code=404, detail="Registro no encontrado")
    return registro

@router.get("/esp/{registro_id}", response_model=schemas.RegistroEsp)
def obtener_registro_esp(registro_id: int, db: Session = Depends(get_db)):
    registro = crud_db.obtener_registro(db, registro_id)
    if not registro:
        raise HTTPException(status_code=404, detail="Registro no encontrado")


    return schemas.RegistroEsp(
        id=registro.id,
        fecha=registro.fecha,
        hora=registro.hora,
        nombre_archivo=registro.nombre_archivo,
        estado=registro.estado,
        probabilidad_sano=registro.probabilidad_sano,
        probabilidad_viral=registro.probabilidad_viral,
        probabilidad_bacteriana=registro.probabilidad_bacteriana,
        username=registro.username,
        radiografia=registro.radiografia
    )

@router.get("/", response_model=List[schemas.RegistroOut])
def obtener_todos_registros(db: Session = Depends(get_db)):
    return crud_db.obtener_todos_registros(db)

@router.put("/{registro_id}", response_model=schemas.RegistroOut)
def actualizar_registro(registro_id: int, registro: schemas.RegistroCreate, db: Session = Depends(get_db)):
    db_registro = crud_db.actualizar_registro(db, registro_id, registro)
    if not db_registro:
        raise HTTPException(status_code=404, detail="Registro no encontrado")
    return db_registro

@router.delete("/{registro_id}")
def eliminar_registro(registro_id: int, db: Session = Depends(get_db)):
    db_registro = crud_db.eliminar_registro(db, registro_id)
    if not db_registro:
        raise HTTPException(status_code=404, detail="Registro no encontrado")
    return {"message": "Registro eliminado"}