from sqlalchemy import Column, Integer, String, Date, Time, Numeric, ForeignKey, LargeBinary, Boolean, text, Text
from sqlalchemy.orm import relationship
from .database_connection import Base

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    username = Column(String(50), unique=True, nullable=False, index=True)
    password = Column(String(255), nullable=False)
    disabled =  Column(Boolean, default=False)
    rol = Column(String(50), nullable=False)

    


class Registro(Base):
    __tablename__ = "registros"

    id = Column(Integer, primary_key=True, index=True)
    fecha = Column(Date, server_default=text("CURRENT_DATE"), nullable=False)
    hora = Column(Time, server_default=text("CURRENT_TIME"), nullable=False)
    nombre_archivo = Column(String(255), nullable=False)
    probabilidad_sano = Column(Numeric(5,2))
    probabilidad_viral = Column(Numeric(5,2))
    probabilidad_bacteriana = Column(Numeric(5,2))
    estado = Column(String(50), nullable=False)
    username = Column(String(50), server_default=text("'Guest'"))
    radiografia = Column(Text)

class Comentario(Base):
    __tablename__ = "comentarios"

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String(150), nullable=False)
    nombre = Column(String(100), nullable=False)
    correo = Column(String(150), nullable=False)
    mensaje = Column(String, nullable=False)

