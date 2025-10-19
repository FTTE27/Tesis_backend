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

# ------------------------------------------------
# TESTS DE USUARIO
# ------------------------------------------------

def test_crear_usuario(db):
    user_data = schemas.UsuarioCreate(
        nombre="Juan Pérez",
        username="juanp",
        rol="user",
        disabled=False,
        password="12345"
    )
    usuario = crud_db.crear_usuario(db, user_data)
    assert usuario is not None
    assert usuario.username == "juanp"
    assert usuario.rol == "user"

def test_obtener_usuario(db):
    usuario = crud_db.obtener_usuario(db, 1)
    assert usuario is not None
    assert usuario.username == "juanp"

def test_obtener_todos_usuarios(db):
    usuarios = crud_db.obtener_todos_usuarios(db)
    assert isinstance(usuarios, list)
    assert len(usuarios) >= 1

def test_actualizar_usuario(db):
    update_data = schemas.UsuarioUpdate(nombre="Juan Actualizado")
    usuario = crud_db.actualizar_usuario(db, 1, update_data)
    assert usuario is not None
    assert usuario.nombre == "Juan Actualizado"

def test_eliminar_usuario(db):
    eliminado = crud_db.eliminar_usuario(db, 1)
    assert eliminado is not None
    assert crud_db.obtener_usuario(db, 1) is None
