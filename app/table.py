from sqlalchemy import Column, Integer, String, Date, Time, Numeric, ForeignKey, LargeBinary, Boolean
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

    registros = relationship("Registro", back_populates="usuario")


class Registro(Base):
    __tablename__ = "registros"

    id = Column(Integer, primary_key=True, index=True)
    fecha = Column(Date, nullable=False)
    hora = Column(Time, nullable=False)
    nombre_archivo = Column(String(255), nullable=False)
    probabilidad_sano = Column(Numeric(5,2))
    probabilidad_viral = Column(Numeric(5,2))
    probabilidad_bacteriana = Column(Numeric(5,2))
    estado = Column(String(50), nullable=False)
    username = Column(String(50), ForeignKey("usuarios.username", ondelete="SET NULL"), default="Guest")
    radiografia = Column(LargeBinary)

    usuario = relationship("Usuario", back_populates="registros")


class Comentario(Base):
    __tablename__ = "comentarios"

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String(150), nullable=False)
    nombre = Column(String(100), nullable=False)
    correo = Column(String(150), nullable=False)
    mensaje = Column(String, nullable=False)

