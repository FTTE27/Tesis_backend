
from fastapi import FastAPI
from app.database_connection import engine, SessionLocal, Base
from app.routers import models, usuarios, auth_users, registros, comentarios

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
from passlib.hash import bcrypt
# Crear las tablas en la base de datos
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

# Lanzar la aplicación
app = FastAPI()


#Routers
app.include_router(models.router) 
app.include_router(auth_users.router)
app.include_router(usuarios.router)
app.include_router(registros.router,)
app.include_router(comentarios.router) 






