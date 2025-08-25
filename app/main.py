from fastapi import FastAPI
from app.database_connection import engine, SessionLocal, Base
from app.routers import models, usuarios, auth_users, registros, comentarios
import uvicorn
from passlib.hash import bcrypt
# Crear las tablas en la base de datos
Base.metadata.create_all(bind=engine)


# Lanzar la aplicación
app = FastAPI()


#Routers
app.include_router(models.router) 
app.include_router(auth_users.router)
app.include_router(usuarios.router)
app.include_router(registros.router,)
app.include_router(comentarios.router) 





