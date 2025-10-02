from sqlalchemy.orm import Session
from app.routers.auth_users import crypt
from . import table, schemas
from passlib.hash import bcrypt
from app.routers.auth_users import crypt
from passlib.context import CryptContext
from fastapi.encoders import jsonable_encoder

crypt = CryptContext(schemes=["bcrypt"], deprecated="auto")

def crear_usuario(db: Session, usuario: schemas.UsuarioCreate):  
    existe = db.query(table.Usuario).filter(table.Usuario.username == usuario.username).first()
    if existe:
        return None  # Ya existe el usuario
    try: 
        hashed_password = crypt.hash(usuario.password)
        usuario_dict = usuario.dict()
        usuario_dict["password"] = hashed_password

        db_user = table.Usuario(**usuario_dict)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    # Error si no dio estan todos los datos obligatorios
    except Exception as e:
        db.rollback()
        return None
    


def obtener_usuario(db: Session, user_id: int):
    return db.query(table.Usuario).filter(table.Usuario.id == user_id).first()

def obtener_todos_usuarios(db: Session):
    return db.query(table.Usuario).all()

def actualizar_usuario(db: Session, user_id: int, usuario: schemas.UsuarioUpdate):
    db_usuario = obtener_usuario(db, user_id)
    if not db_usuario:
        return None
     # solo los campos que realmente se enviaron en la petición
    update_data = usuario.dict(exclude_unset=True) 

    # Si viene contraseña y no está vacía, la encriptamos
    if "password" in update_data and update_data["password"]:
        update_data["password"] = crypt.hash(update_data["password"])
    elif "password" in update_data and not update_data["password"]:
        # Si mandan password vacío, lo quitamos para no sobreescribir
        update_data.pop("password")

    # Aplicamos los cambios desde update_data (no desde usuario.dict())
    for key, value in update_data.items():
        setattr(db_usuario, key, value)
        
    db.commit()
    db.refresh(db_usuario)
    return db_usuario

def eliminar_usuario(db: Session, user_id: int):
    db_usuario = obtener_usuario(db, user_id)
    if not db_usuario:
        return None
    db.delete(db_usuario)
    db.commit()
    return db_usuario

def crear_registro(db: Session, registro: schemas.RegistroCreate, username: str):
    db_registro = table.Registro(
        nombre_archivo=registro.nombre_archivo,
        probabilidad_sano=registro.probabilidad_sano,
        probabilidad_viral=registro.probabilidad_viral,
        probabilidad_bacteriana=registro.probabilidad_bacteriana,
        estado=registro.estado,
        username=username,
        radiografia=registro.radiografia
    )
    db.add(db_registro)
    db.commit()
    db.refresh(db_registro)
    return db_registro


def obtener_registro(db: Session, registro_id: int):
    return db.query(table.Registro).filter(table.Registro.id == registro_id).first()

def obtener_todos_registros(db: Session):
    return db.query(table.Registro).all()

def actualizar_registro(db: Session, registro_id: int, registro: schemas.RegistroCreate):
    db_registro = obtener_registro(db, registro_id)
    if not db_registro:
        return None
    for key, value in registro.dict().items():
        setattr(db_registro, key, value)
    db.commit()
    db.refresh(db_registro)
    return db_registro

def eliminar_registro(db: Session, registro_id: int):
    db_registro = obtener_registro(db, registro_id)
    if not db_registro:
        return None
    db.delete(db_registro)
    db.commit()
    return db_registro

def crear_comentario(db: Session, comentario: schemas.ComentarioCreate):
    db_comentario = table.Comentario(**comentario.dict())
    db.add(db_comentario)
    db.commit()
    db.refresh(db_comentario)
    return db_comentario

def obtener_comentario(db: Session, comentario_id: int):
    return db.query(table.Comentario).filter(table.Comentario.id == comentario_id).first()

def obtener_todos_comentarios(db: Session):
    return db.query(table.Comentario).all()

def actualizar_comentario(db: Session, comentario_id: int, comentario: schemas.ComentarioCreate):
    db_comentario = obtener_comentario(db, comentario_id)
    if not db_comentario:
        return None
    for key, value in comentario.dict().items():
        setattr(db_comentario, key, value)
    db.commit()
    db.refresh(db_comentario)
    return db_comentario

def eliminar_comentario(db: Session, comentario_id: int):
    db_comentario = obtener_comentario(db, comentario_id)
    if not db_comentario:
        return None
    db.delete(db_comentario)
    db.commit()
    return db_comentario
