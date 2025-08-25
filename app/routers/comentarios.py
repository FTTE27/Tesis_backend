from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlalchemy.orm import Session
from app import schemas, crud_db
from app.database_connection import get_db

router = APIRouter(
    prefix="/comentarios",
    tags=["Comentarios"],
    responses={status.HTTP_404_NOT_FOUND: {"message": "No encontrado"}}
)


@router.post("/", response_model=schemas.ComentarioOut)
def crear_comentario(comentario: schemas.ComentarioCreate, db: Session = Depends(get_db)):
    return crud_db.crear_comentario(db, comentario)


@router.get("/{comentario_id}", response_model=schemas.ComentarioOut)
def obtener_comentario(comentario_id: int, db: Session = Depends(get_db)):
    comentario = crud_db.obtener_comentario(db, comentario_id)
    if not comentario:
        raise HTTPException(status_code=404, detail="Comentario no encontrado")
    return comentario


@router.get("/", response_model=List[schemas.ComentarioOut])
def obtener_todos_comentarios(db: Session = Depends(get_db)):
    return crud_db.obtener_todos_comentarios(db)



@router.put("/{comentario_id}", response_model=schemas.ComentarioOut)
def actualizar_comentario(comentario_id: int, comentario: schemas.ComentarioCreate, db: Session = Depends(get_db)):
    db_comentario = crud_db.actualizar_comentario(db, comentario_id, comentario)
    if not db_comentario:
        raise HTTPException(status_code=404, detail="Comentario no encontrado")
    return db_comentario

@router.delete("/{comentario_id}")
def eliminar_comentario(comentario_id: int, db: Session = Depends(get_db)):
    db_comentario = crud_db.eliminar_comentario(db, comentario_id)
    if not db_comentario:
        raise HTTPException(status_code=404, detail="Comentario no encontrado")
    return {"message": "Comentario eliminado"}