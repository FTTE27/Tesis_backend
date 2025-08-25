from typing import List
from fastapi import FastAPI, UploadFile, File, Form, HTTPException, Depends
from fastapi.responses import JSONResponse
from app.classifier import ImageClassifier
from sqlalchemy.orm import Session
from . import table, schemas, crud_db
from .database_connection import engine, SessionLocal, Base

import os
import shutil
import uvicorn

Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


MODELS_DIR = "models"
CLASS_NAMES = ["BAC_PNEUMONIA", "NORMAL", "VIR_PNEUMONIA"]

classifier = ImageClassifier(os.path.join(MODELS_DIR, "densenet_no_encapsulado.keras"), class_names=CLASS_NAMES)

@app.post("/usuarios/", response_model=schemas.UsuarioOut)
async def crear_usuario(usuario: schemas.UsuarioCreate, db: Session = Depends(get_db)):
    return crud_db.crear_usuario(db, usuario)

@app.get("/usuarios/{user_id}", response_model=schemas.UsuarioOut)
async def obtener_usuario(user_id: int, db: Session = Depends(get_db)):
    usuario = crud_db.obtener_usuario(db, user_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario

@app.get("/usuarios/", response_model=List[schemas.UsuarioOut])
async def obtener_todos_usuarios(db: Session = Depends(get_db)):
    return crud_db.obtener_todos_usuarios(db)

@app.put("/usuarios/{user_id}", response_model=schemas.UsuarioOut)
async def actualizar_usuario(user_id: int, usuario: schemas.UsuarioCreate, db: Session = Depends(get_db)):
    db_usuario = crud_db.actualizar_usuario(db, user_id, usuario)
    if not db_usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return db_usuario

@app.delete("/usuarios/{user_id}")
async def eliminar_usuario(user_id: int, db: Session = Depends(get_db)):
    db_usuario = crud_db.eliminar_usuario(db, user_id)
    if not db_usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return {"message": "Usuario eliminado"}


@app.post("/registros/", response_model=schemas.RegistroOut)
async def crear_registro(registro: schemas.RegistroCreate, db: Session = Depends(get_db)):
    return crud_db.crear_registro(db, registro)

@app.get("/registros/{registro_id}", response_model=schemas.RegistroOut)
async def obtener_registro(registro_id: int, db: Session = Depends(get_db)):
    registro = crud_db.obtener_registro(db, registro_id)
    if not registro:
        raise HTTPException(status_code=404, detail="Registro no encontrado")
    return registro

@app.get("/registros/", response_model=List[schemas.RegistroOut])
async def obtener_todos_registros(db: Session = Depends(get_db)):
    return crud_db.obtener_todos_registros(db)

@app.put("/registros/{registro_id}", response_model=schemas.RegistroOut)
async def actualizar_registro(registro_id: int, registro: schemas.RegistroCreate, db: Session = Depends(get_db)):
    db_registro = crud_db.actualizar_registro(db, registro_id, registro)
    if not db_registro:
        raise HTTPException(status_code=404, detail="Registro no encontrado")
    return db_registro

@app.delete("/registros/{registro_id}")
async def eliminar_registro(registro_id: int, db: Session = Depends(get_db)):
    db_registro = crud_db.eliminar_registro(db, registro_id)
    if not db_registro:
        raise HTTPException(status_code=404, detail="Registro no encontrado")
    return {"message": "Registro eliminado"}

@app.post("/comentarios/", response_model=schemas.ComentarioOut)
async def crear_comentario(comentario: schemas.ComentarioCreate, db: Session = Depends(get_db)):
    return crud_db.crear_comentario(db, comentario)

@app.get("/comentarios/{comentario_id}", response_model=schemas.ComentarioOut)
async def obtener_comentario(comentario_id: int, db: Session = Depends(get_db)):
    comentario = crud_db.obtener_comentario(db, comentario_id)
    if not comentario:
        raise HTTPException(status_code=404, detail="Comentario no encontrado")
    return comentario

@app.get("/comentarios/", response_model=List[schemas.ComentarioOut])
async def obtener_todos_comentarios(db: Session = Depends(get_db)):
    return crud_db.obtener_todos_comentarios(db)

@app.put("/comentarios/{comentario_id}", response_model=schemas.ComentarioOut)
async def actualizar_comentario(comentario_id: int, comentario: schemas.ComentarioCreate, db: Session = Depends(get_db)):
    db_comentario = crud_db.actualizar_comentario(db, comentario_id, comentario)
    if not db_comentario:
        raise HTTPException(status_code=404, detail="Comentario no encontrado")
    return db_comentario

@app.delete("/comentarios/{comentario_id}")
async def eliminar_comentario(comentario_id: int, db: Session = Depends(get_db)):
    db_comentario = crud_db.eliminar_comentario(db, comentario_id)
    if not db_comentario:
        raise HTTPException(status_code=404, detail="Comentario no encontrado")
    return {"message": "Comentario eliminado"}

@app.post("/predecir")
async def predecir(file: UploadFile = File(...)):
    if not file.filename.lower().endswith((".png", ".jpg", ".jpeg")):
        raise HTTPException(status_code=400, detail="La radiografía debe ser tipo .png, .jpg o .jpeg")
    
    try:
        image_bytes = await file.read()
        prediccion = classifier.predict(image_bytes)
        return prediccion
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error procesando la imagen: {str(e)}")

@app.post("/predecir_con_heatmap")
async def predecir_con_heatmap(file: UploadFile = File(...)):
    """
    Endpoint para obtener la predicción junto con el mapa de calor
    """
    if not file.filename.lower().endswith((".png", ".jpg", ".jpeg")):
        raise HTTPException(status_code=400, detail="La radiografía debe ser tipo .png, .jpg o .jpeg")
    
    try:
        image_bytes = await file.read()
        prediccion = classifier.predict_heatmap(image_bytes)
        return JSONResponse(content=prediccion)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error procesando la imagen: {str(e)}")
    