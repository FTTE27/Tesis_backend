from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from app.classifier import ImageClassifier
import os
import shutil

app = FastAPI()

MODELS_DIR = "models"

# Modelo inicial
classifier = ImageClassifier(os.path.join(MODELS_DIR, "densenet.keras"))

@app.post("/predict")
async def predict_image(file: UploadFile = File(...)):
    if not file.filename.endswith(".png") and not file.filename.endswith(".jpg") and not file.filename.endswith(".jpeg"):
        raise HTTPException(status_code=400, detail="La radiografía debe ser tipo .png, .jpg o .jpeg")
    
    image_bytes = await file.read()
    prediction = classifier.predict(image_bytes)
    return {"prediction": prediction}

@app.post("/predict_with_heatmap")
async def predict_with_heatmap(file: UploadFile = File(...)):
    if not file.filename.endswith(".png") and not file.filename.endswith(".jpg") and not file.filename.endswith(".jpeg"):
        raise HTTPException(status_code=400, detail="La radiografía debe ser tipo .png, .jpg o .jpeg")

    image_bytes = await file.read()
    result = classifier.get_prediction_with_heatmap(image_bytes)
    return result

@app.post("/change_model")
async def change_model(model_name: str = Form(...)):
    model_path = os.path.join(MODELS_DIR, model_name)
    if not os.path.exists(model_path):
        raise HTTPException(status_code=404, detail="Modelo no encontrado")
    
    classifier.change_model(model_path)
    return {"message": f"Modelo cambiado a {model_name}"}

@app.post("/upload_model")
async def upload_model(file: UploadFile = File(...)):
    if not file.filename.endswith(".keras"):
        raise HTTPException(status_code=400, detail="El modelo debe ser un archivo .keras")
    
    save_path = os.path.join(MODELS_DIR, file.filename)
    with open(save_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {"message": f"Modelo {file.filename} subido correctamente"}
