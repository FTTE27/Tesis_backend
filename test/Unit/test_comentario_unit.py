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
# TESTS DE COMENTARIO
# ------------------------------------------------

def test_crear_comentario(db):
    comentario_data = schemas.ComentarioCreate(
        nombre="Andrés López",
        titulo="Comentario de prueba",
        correo="andres@prueba.com",
        mensaje="Todo funciona correctamente."
    )
    nuevo_comentario = crud_db.crear_comentario(db, comentario_data)
    assert nuevo_comentario.id is not None
    assert nuevo_comentario.nombre == "Andrés López"
    assert nuevo_comentario.titulo == "Comentario de prueba"

def test_obtener_comentario(db):
    comentario = crud_db.obtener_comentario(db, 1)
    assert comentario is not None
    assert comentario.nombre == "Andrés López"

def test_obtener_todos_comentarios(db):
    comentarios = crud_db.obtener_todos_comentarios(db)
    assert isinstance(comentarios, list)
    assert len(comentarios) >= 1

def test_actualizar_comentario(db):
    data = schemas.ComentarioCreate(
        nombre="Andrés Actualizado",
        titulo="Título actualizado",
        correo="andres@update.com",
        mensaje="Comentario actualizado correctamente."
    )
    comentario = crud_db.actualizar_comentario(db, 1, data)
    assert comentario is not None
    assert comentario.nombre == "Andrés Actualizado"

def test_eliminar_comentario(db):
    eliminado = crud_db.eliminar_comentario(db, 1)
    assert eliminado is not None
    assert crud_db.obtener_comentario(db, 1) is None
