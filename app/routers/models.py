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
MODELS_DIR = "classification_models"
CLASS_NAMES = ["BAC_PNEUMONIA", "NORMAL", "VIR_PNEUMONIA"]  

# Modelo inicial
classifier = ImageClassifier(os.path.join(MODELS_DIR, "DN.keras"), class_names=CLASS_NAMES)

actual_model = "DN.keras"

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
        result = classifier.predict_heatmap(image_bytes)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generando heatmap: {str(e)}")

@router.post("/predict_with_heatmap_first")
async def predict_with_heatmap(file: UploadFile = File(...)):
    if not file.filename.lower().endswith((".png", ".jpg", ".jpeg")):
        raise HTTPException(status_code=400, detail="La radiografía debe ser tipo .png, .jpg o .jpeg")

    try:
        image_bytes = await file.read()
        result = classifier.predict_heatmap_principio(image_bytes)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generando heatmap: {str(e)}")


@router.post("/change_model")
async def change_model(model_name: str = Form(...)):
    global classifier, actual_model   
    model_path = os.path.join(MODELS_DIR, model_name)
    
    if not os.path.exists(model_path):
        raise HTTPException(status_code=404, detail="Modelo no encontrado")
    
    try:
        classifier = ImageClassifier(model_path, class_names=CLASS_NAMES)
        actual_model = model_name
        return {"message": f"Modelo cambiado a {model_name}", "status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error cargando modelo: {str(e)}")
    
@router.get("/get_models")
async def get_models():
    try:
        if not os.path.exists(MODELS_DIR):
            raise HTTPException(status_code=404, detail="La carpeta de modelos no existe")
        
        models = [f for f in os.listdir(MODELS_DIR) if f.endswith((".keras", ".h5", ".pkl"))]
        
        if not models:
            return {"message": "No hay modelos disponibles en la carpeta", "models": []}
        
        return {"models": models}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error listando modelos: {str(e)}")

@router.get("/model_info")
async def model_info():
    return {
        "current_model": actual_model,
        "class_names": CLASS_NAMES,
        "input_shape": (224, 224, 3)  
    }