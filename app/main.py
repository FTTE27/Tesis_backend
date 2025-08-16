from fastapi import FastAPI

app = FastAPI(title="Mi API con FastAPI", version="1.0")

@app.get("/")
def read_root():
    
    return {"mensaje": "Hola, FastAPI funcionando!"}
