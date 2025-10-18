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

def test_crear_registro(db):
    data = schemas.RegistroCreate(
        nombre_archivo="radiografia1.png",
        probabilidad_sano=0.85,
        probabilidad_viral=0.10,
        probabilidad_bacteriana=0.05,
        estado="DN.keras",
        radiografia="prueba"
    )
    registro = crud_db.crear_registro(db, data, username="juan")
    assert registro is not None
    assert registro.nombre_archivo == "radiografia1.png"

def test_obtener_registro(db):
    registro = crud_db.obtener_registro(db, 1)
    assert registro is not None
    assert registro.estado == "sano"

def test_obtener_todos_registros(db):
    registros = crud_db.obtener_todos_registros(db)
    assert len(registros) >= 1

def test_actualizar_registro(db):
    data = schemas.RegistroCreate(
        nombre_archivo="radiografia2.png",
        probabilidad_sano=0.70,
        probabilidad_viral=0.20,
        probabilidad_bacteriana=0.10,
        estado="CNN.keras",
        radiografia="prueba"
    )
    registro = crud_db.actualizar_registro(db, 1, data)
    assert registro.estado == "CNN.keras"

def test_eliminar_registro(db):
    eliminado = crud_db.eliminar_registro(db, 1)
    assert eliminado is not None
    assert crud_db.obtener_registro(db, 1) is None
