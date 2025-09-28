from pydantic import BaseModel, StringConstraints
from datetime import date, time
from typing import Optional, Annotated


class UsuarioBase(BaseModel):
    nombre: Annotated[str, StringConstraints(min_length=1, max_length=100)]
    username: Annotated[str, StringConstraints(min_length=1, max_length=50)]
    rol: Annotated[str, StringConstraints(min_length=1, max_length=50)]
    disabled: bool

class UsuarioCreate(UsuarioBase):
    password: Annotated[str, StringConstraints(min_length=1, max_length=255)]

class UsuarioUpdate(BaseModel):
    nombre: Optional[str] = None
    username: Optional[str] = None
    password: Optional[str] = None

class UsuarioOut(UsuarioBase):
    id: int
    class Config:
        from_attributes = True

class RegistroBase(BaseModel):
    nombre_archivo: str
    estado: str
    probabilidad_sano: Optional[float] = None
    probabilidad_viral: Optional[float] = None
    probabilidad_bacteriana: Optional[float] = None
    username: Optional[str] = "Guest"


class RegistroCreate(RegistroBase):
    radiografia: str

class RegistroOut(RegistroBase):
    id: int
    fecha: date
    hora: time
    class Config:
        orm_mode = True

class RegistroEsp(RegistroBase):
    id: int
    fecha: date
    hora: time
    radiografia: str | None
    class Config:
        orm_mode = True

class ComentarioBase(BaseModel):
    nombre: str
    titulo: str
    correo: str
    mensaje: str

class ComentarioCreate(ComentarioBase):
    pass

class ComentarioOut(ComentarioBase):
    id: int
    class Config:
        orm_mode = True
