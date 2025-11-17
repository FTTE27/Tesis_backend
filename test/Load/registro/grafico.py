import json
import pandas as pd
import matplotlib.pyplot as plt

with open("registro_create.json", "r", encoding="utf-8") as f:
    data = [json.loads(line) for line in f]

duraciones = []
for d in data:
    if d.get("type") == "Point" and d.get("metric") == "http_req_duration":
        valor = None
        if "value" in d:
            valor = d["value"]
        elif "data" in d and "value" in d["data"]:
            valor = d["data"]["value"]
        if valor is not None:
            duraciones.append(valor)

duraciones = duraciones[:200]
df = pd.DataFrame({"Duración (ms)": duraciones})

if df.empty:
    print("No se encontraron métricas http_req_duration en el JSON.")
else:
    print(f"{len(df)} registros cargados correctamente.")

    # Gráfico 1: Duración por solicitud 
    plt.figure()
    plt.plot(df["Duración (ms)"])
    plt.title("Duración de solicitudes HTTP (http_req_duration)")
    plt.xlabel("Número de solicitud")
    plt.ylabel("Tiempo (ms)")
    plt.grid(True)
    plt.show()

    # Gráfico 2: Histograma 
    plt.figure()
    plt.hist(df["Duración (ms)"], bins=20, edgecolor="black")
    plt.title("Distribución de tiempos de respuesta")
    plt.xlabel("Duración (ms)")
    plt.ylabel("Frecuencia")
    plt.grid(True)
    plt.show()

    # Estadísticas básicas 
    print("\nEstadísticas de duración:")
    print(df.describe())
