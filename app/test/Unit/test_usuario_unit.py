import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app import table, schemas, crud_db

SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="module")
def db():
    table.Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    yield db
    db.close()
    table.Base.metadata.drop_all(bind=engine)

def test_crear_usuario(db):
    user_data = schemas.UsuarioCreate(
        username="juan",
        password="12345",
        correo="juan@gmail.com",
        rol="user"
    )
    usuario = crud_db.crear_usuario(db, user_data)
    assert usuario is not None
    assert usuario.username == "juan"

def test_obtener_usuario(db):
    usuario = crud_db.obtener_usuario(db, 1)
    assert usuario.username == "juan"

def test_obtener_todos_usuarios(db):
    usuarios = crud_db.obtener_todos_usuarios(db)
    assert len(usuarios) == 1

def test_actualizar_usuario(db):
    update_data = schemas.UsuarioUpdate(correo="nuevo@example.com")
    usuario = crud_db.actualizar_usuario(db, 1, update_data)
    assert usuario.correo == "nuevo@example.com"

def test_eliminar_usuario(db):
    eliminado = crud_db.eliminar_usuario(db, 1)
    assert eliminado is not None
    assert crud_db.obtener_usuario(db, 1) is None
