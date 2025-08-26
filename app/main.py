
from fastapi import FastAPI
from app.database_connection import engine, SessionLocal, Base
from app.routers import models, usuarios, auth_users, registros, comentarios

from typing import List
from fastapi import FastAPI, UploadFile, File, Form, HTTPException, Depends
from fastapi.responses import JSONResponse
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

# Lanzar la aplicación
app = FastAPI()


#Routers
app.include_router(models.router) 
app.include_router(auth_users.router)
app.include_router(usuarios.router)
app.include_router(registros.router,)
app.include_router(comentarios.router) 






