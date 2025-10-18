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

def test_crear_comentario(db):
    comentario_data = schemas.ComentarioCreate(
        contenido="Prueba de comentario",
        username="andres",
        registro_id=1
    )
    nuevo_comentario = crud_db.crear_comentario(db, comentario_data)
    assert nuevo_comentario.id is not None
    assert nuevo_comentario.contenido == "Prueba de comentario"

def test_obtener_comentario(db):
    comentario = crud_db.obtener_comentario(db, 1)
    assert comentario is not None
    assert comentario.contenido == "Prueba de comentario"

def test_obtener_todos_comentarios(db):
    comentarios = crud_db.obtener_todos_comentarios(db)
    assert len(comentarios) >= 1

def test_actualizar_comentario(db):
    data = schemas.ComentarioCreate(
        contenido="Actualizado correctamente",
        username="andres",
        registro_id=1
    )
    comentario = crud_db.actualizar_comentario(db, 1, data)
    assert comentario.contenido == "Actualizado correctamente"

def test_eliminar_comentario(db):
    eliminado = crud_db.eliminar_comentario(db, 1)
    assert eliminado is not None
    assert crud_db.obtener_comentario(db, 1) is None
