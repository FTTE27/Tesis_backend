# Tesis_backend

1. Generar el entorno virtual de python (si ya esta venv no es necesario)
python -m venv venv

2. Activar el entorno virtual
venv\Scripts\activate

3. Instalar o actualizar fastapi
pip install fastapi uvicorn

4. Instalar o actualizar keras 
pip install keras

5. Instalar o actualizar tensorflow
pip install tensorflow

6. Instalar o actualizar matplotlib
pip install matplotlib

7. Ejecutar el servidor
uvicorn app.main:app --reload

8. Se ejecuta de manera predeterminada en http://127.0.0.1:8000