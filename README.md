# Tesis_backend

1. Generar el entorno virtual de python (si ya esta venv no es necesario)
python -m venv venv

2. Activar el entorno virtual
venv\Scripts\activate

3. Instalar requirements.txt
pip install -r requirements.txt

4. Ejecutar el servidor
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

5. Se ejecuta de manera predeterminada en http://127.0.0.1:8000

// Pruebas

Para el desarrollo de las pruebas se tienen las siguientes recomendaciones:
    Unit
    1. Las pruebas se ejecutan con cada script de python.
    2. Al ser pruebas de únicamente el modulo, no necesita de iniciar el sistema backend para ser realizadas.

    Load
    1. Se requiere de tener k6 en el equipo.
    2. Las pruebas se separan por los principales métodos de los endpoints para facilitar las operaciones.
    3. Se ejecuta test_{nombre del modulo} para ejecutar todas las pruebas del módulo.