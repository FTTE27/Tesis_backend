import io
from fastapi.testclient import TestClient

IMAGE_PATH = "test/Integration/IM-0001-0001.jpeg"

def test_predict_and_save_register(client):
    
    with open(IMAGE_PATH, "rb") as f:
        response = client.post("/models/predict_with_heatmap", files={'files': f})
    assert response.status_code in (200)  
