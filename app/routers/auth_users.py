from .. import table as db_models
from passlib.hash import bcrypt
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from .. import schemas
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from ..database_connection import get_db
from sqlalchemy.orm import Session
# Algoritmo de encriptación
ALGORITHM = "HS256"
# Tiempo de duración del token en minutos
ACCESS_TOKEN_DURATION = 15

# Router 
router = APIRouter(
    prefix="/auth",
    tags=["Autenticación"],
    responses={status.HTTP_404_NOT_FOUND: {"message": "No encontrado"}}
)

oauth2 = OAuth2PasswordBearer(tokenUrl="auth/login")

# Contexto de encriptación
crypt = CryptContext(schemes=["bcrypt"])

# Clave secreta para la creación del token
SECRET = "201d573bd7d1344d3a3bfce1550b69102fd11be3db6d379508b6cccc58ea230b"


# buscar usuario en la base de datos exponiendo la contraseña
def buscar_usuario_db(username: str, db: Session):
    return db.query(db_models.Usuario).filter(db_models.Usuario.username == username).first()

# Buscar usuario sin exponer contraseña
def buscar_usuario(username: str, db: Session):
    user = db.query(db_models.Usuario).filter(db_models.Usuario.username == username).first()
    if user:
        return schemas.UsuarioOut.from_orm(user)

 
# Validar usuario autenticado   
async def usuario_autenticado(token: str = Depends(oauth2), db: Session = Depends(get_db)):

    exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credenciales de autenticación inválidas",
        headers={"WWW-Authenticate": "Bearer"})

    try:
        username = jwt.decode(token, SECRET, algorithms=[ALGORITHM]).get("sub")
        if username is None:
            raise exception

    except JWTError:
        raise exception
    return buscar_usuario(username, db) 
    

# Obtener usuario actual solo si esta autenticado    
async def usuario_actual(user: schemas.UsuarioOut = Depends(usuario_autenticado)):
    if user.disabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Usuario inactivo")
    return user

#Login
@router.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # buscar el usuario en la base de datos
    user_db = buscar_usuario(form.username, db)
    if not user_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="El usuario no es correcto")

    # buscar el usuario en la base de datos exponiendo la contraseña para comparar contraseñas
    user = buscar_usuario_db(form.username, db)

    if not crypt.verify(form.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="La contraseña no es correcta")
    # Crear el token de acceso con la información del usuario y tiempo de expiración
    access_token = {"sub": user.username,
                    "exp": datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_DURATION)}
    # Retornar el token de acceso
    return {"access_token": jwt.encode(access_token, SECRET, algorithm=ALGORITHM), "token_type": "bearer"}

@router.get("/me")
async def get_profile(user: schemas.UsuarioOut = Depends(usuario_actual)):
    return user