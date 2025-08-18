from typing import List
from fastapi import FastAPI, UploadFile, File, Form, HTTPException, Depends
from app.classifier import ImageClassifier
from sqlalchemy.orm import Session
from . import table, schemas, crud_db
from .database_connection import engine, SessionLocal, Base

import os
import shutil
import uvicorn

Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


MODELS_DIR = "models"
CLASS_NAMES = ["BAC_PNEUMONIA", "NORMAL", "VIR_PNEUMONIA"]

# Modelo inicial
# classifier = ImageClassifier(os.path.join(MODELS_DIR, "densenet.h5"), class_names=CLASS_NAMES)

@app.post("/usuarios/", response_model=schemas.UsuarioOut)
def crear_usuario(usuario: schemas.UsuarioCreate, db: Session = Depends(get_db)):
    return crud_db.crear_usuario(db, usuario)

@app.get("/usuarios/{user_id}", response_model=schemas.UsuarioOut)
def obtener_usuario(user_id: int, db: Session = Depends(get_db)):
    usuario = crud_db.obtener_usuario(db, user_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario

@app.get("/usuarios/", response_model=List[schemas.UsuarioOut])
def obtener_todos_usuarios(db: Session = Depends(get_db)):
    return crud_db.obtener_todos_usuarios(db)

@app.put("/usuarios/{user_id}", response_model=schemas.UsuarioOut)
def actualizar_usuario(user_id: int, usuario: schemas.UsuarioCreate, db: Session = Depends(get_db)):
    db_usuario = crud_db.actualizar_usuario(db, user_id, usuario)
    if not db_usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return db_usuario

@app.delete("/usuarios/{user_id}")
def eliminar_usuario(user_id: int, db: Session = Depends(get_db)):
    db_usuario = crud_db.eliminar_usuario(db, user_id)
    if not db_usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return {"message": "Usuario eliminado"}


@app.post("/registros/", response_model=schemas.RegistroOut)
def crear_registro(registro: schemas.RegistroCreate, db: Session = Depends(get_db)):
    return crud_db.crear_registro(db, registro)

@app.get("/registros/{registro_id}", response_model=schemas.RegistroOut)
def obtener_registro(registro_id: int, db: Session = Depends(get_db)):
    registro = crud_db.obtener_registro(db, registro_id)
    if not registro:
        raise HTTPException(status_code=404, detail="Registro no encontrado")
    return registro

@app.get("/registros/", response_model=List[schemas.RegistroOut])
def obtener_todos_registros(db: Session = Depends(get_db)):
    return crud_db.obtener_todos_registros(db)

@app.put("/registros/{registro_id}", response_model=schemas.RegistroOut)
def actualizar_registro(registro_id: int, registro: schemas.RegistroCreate, db: Session = Depends(get_db)):
    db_registro = crud_db.actualizar_registro(db, registro_id, registro)
    if not db_registro:
        raise HTTPException(status_code=404, detail="Registro no encontrado")
    return db_registro

@app.delete("/registros/{registro_id}")
def eliminar_registro(registro_id: int, db: Session = Depends(get_db)):
    db_registro = crud_db.eliminar_registro(db, registro_id)
    if not db_registro:
        raise HTTPException(status_code=404, detail="Registro no encontrado")
    return {"message": "Registro eliminado"}

@app.post("/comentarios/", response_model=schemas.ComentarioOut)
def crear_comentario(comentario: schemas.ComentarioCreate, db: Session = Depends(get_db)):
    return crud_db.crear_comentario(db, comentario)

@app.get("/comentarios/{comentario_id}", response_model=schemas.ComentarioOut)
def obtener_comentario(comentario_id: int, db: Session = Depends(get_db)):
    comentario = crud_db.obtener_comentario(db, comentario_id)
    if not comentario:
        raise HTTPException(status_code=404, detail="Comentario no encontrado")
    return comentario

@app.get("/comentarios/", response_model=List[schemas.ComentarioOut])
def obtener_todos_comentarios(db: Session = Depends(get_db)):
    return crud_db.obtener_todos_comentarios(db)

@app.put("/comentarios/{comentario_id}", response_model=schemas.ComentarioOut)
def actualizar_comentario(comentario_id: int, comentario: schemas.ComentarioCreate, db: Session = Depends(get_db)):
    db_comentario = crud_db.actualizar_comentario(db, comentario_id, comentario)
    if not db_comentario:
        raise HTTPException(status_code=404, detail="Comentario no encontrado")
    return db_comentario

@app.delete("/comentarios/{comentario_id}")
def eliminar_comentario(comentario_id: int, db: Session = Depends(get_db)):
    db_comentario = crud_db.eliminar_comentario(db, comentario_id)
    if not db_comentario:
        raise HTTPException(status_code=404, detail="Comentario no encontrado")
    return {"message": "Comentario eliminado"}

@app.post("/predict")
async def predict_image(file: UploadFile = File(...)):
    if not file.filename.lower().endswith((".png", ".jpg", ".jpeg")):
        raise HTTPException(status_code=400, detail="La radiografía debe ser tipo .png, .jpg o .jpeg")
    
    try:
        image_bytes = await file.read()
        prediction = classifier.predict(image_bytes)
        return {
            "predictions": {
                CLASS_NAMES[0]: prediction[0][0],
                CLASS_NAMES[1]: prediction[0][1],
                CLASS_NAMES[2]: prediction[0][2],
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error procesando la imagen: {str(e)}")

@app.post("/predict_with_heatmap")
async def predict_with_heatmap(file: UploadFile = File(...)):
    if not file.filename.lower().endswith((".png", ".jpg", ".jpeg")):
        raise HTTPException(status_code=400, detail="La radiografía debe ser tipo .png, .jpg o .jpeg")

    try:
        image_bytes = await file.read()
        result = classifier.get_prediction_with_heatmap(image_bytes)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generando heatmap: {str(e)}")

@app.post("/change_model")
async def change_model(model_name: str = Form(...)):
    model_path = os.path.join(MODELS_DIR, model_name)
    if not os.path.exists(model_path):
        raise HTTPException(status_code=404, detail="Modelo no encontrado")
    
    try:
        classifier.change_model(model_path)
        return {"message": f"Modelo cambiado a {model_name}", "status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error cargando modelo: {str(e)}")

@app.post("/upload_model")
async def upload_model(file: UploadFile = File(...)):
    if not file.filename.lower().endswith((".h5", ".keras", ".pb")):
        raise HTTPException(status_code=400, detail="Formato de modelo no soportado. Use .h5, .keras o SavedModel")
    
    try:
        save_path = os.path.join(MODELS_DIR, file.filename)
        with open(save_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        return {"message": f"Modelo {file.filename} subido correctamente", "path": save_path}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error subiendo modelo: {str(e)}")

@app.get("/model_info")
async def model_info():
    return {
        "current_model": os.path.basename(classifier.model_path),
        "class_names": CLASS_NAMES,
        "input_shape": (224, 224, 1)  
    }

