from pydantic import BaseModel
from datetime import date, time
from typing import Optional


class UsuarioBase(BaseModel):
    nombre: str
    username: str
    rol: str

class UsuarioCreate(UsuarioBase):
    contraseña: str

class UsuarioOut(UsuarioBase):
    id: int
    class Config:
        orm_mode = True


class RegistroBase(BaseModel):
    fecha: date
    hora: time
    nombre_archivo: str
    estado: str
    probabilidad_sano: Optional[float] = None
    probabilidad_viral: Optional[float] = None
    probabilidad_bacteriana: Optional[float] = None
    username: Optional[str] = "Guest"

class RegistroCreate(RegistroBase):
    pass

class RegistroOut(RegistroBase):
    id: int
    class Config:
        orm_mode = True


class ComentarioBase(BaseModel):
    nombre: str
    correo: str
    mensaje: str

class ComentarioCreate(ComentarioBase):
    pass

class ComentarioOut(ComentarioBase):
    id: int
    class Config:
        orm_mode = True
