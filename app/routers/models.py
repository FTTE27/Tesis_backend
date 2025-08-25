from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form, HTTPException
from app.classifier import ImageClassifier
import os
import shutil

# Router 
router = APIRouter(
    prefix="/models",
    tags=["Modelos"],
    responses={status.HTTP_404_NOT_FOUND: {"message": "No encontrado"}}
)

#Carpetas donde se guardaran los modelos
MODELS_DIR = "models"
CLASS_NAMES = ["BAC_PNEUMONIA", "NORMAL", "VIR_PNEUMONIA"]  

# Modelo inicial
#classifier = ImageClassifier(os.path.join(MODELS_DIR, "densenet3.keras"), class_names=CLASS_NAMES)


@router.post("/predict")
async def predict_image(file: UploadFile = File(...)):
    if not file.filename.lower().endswith((".png", ".jpg", ".jpeg")):
        raise HTTPException(status_code=400, detail="La radiografía debe ser tipo .png, .jpg o .jpeg")
    
    try:
        image_bytes = await file.read()
        prediction = classifier.predict(image_bytes)
        return prediction
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error procesando la imagen: {str(e)}")

    
@router.post("/predict_with_heatmap")
async def predict_with_heatmap(file: UploadFile = File(...)):
    if not file.filename.lower().endswith((".png", ".jpg", ".jpeg")):
        raise HTTPException(status_code=400, detail="La radiografía debe ser tipo .png, .jpg o .jpeg")

    try:
        image_bytes = await file.read()
        result = classifier.get_prediction_with_heatmap(image_bytes)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generando heatmap: {str(e)}")


@router.post("/change_model")
async def change_model(model_name: str = Form(...)):
    model_path = os.path.join(MODELS_DIR, model_name)
    if not os.path.exists(model_path):
        raise HTTPException(status_code=404, detail="Modelo no encontrado")
    
    try:
        classifier.change_model(model_path)
        return {"message": f"Modelo cambiado a {model_name}", "status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error cargando modelo: {str(e)}")


@router.post("/upload_model")
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
    
    
@router.get("/model_info")
async def model_info():
    return {
        "current_model": os.path.basename(classifier.model_path),
        "class_names": CLASS_NAMES,
        "input_shape": (224, 224, 1)  
    }