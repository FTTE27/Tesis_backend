def test_usuario_crea_registro(client):
    # Creación de un usuario
    user_data = {
        "nombre": "Laura",
        "username": "laura123",
        "password": "abcde",
        "rol": "usuario",
        "disabled": False
    }
    user_resp = client.post("/usuarios/", json=user_data)
    assert user_resp.status_code == 200
    user = user_resp.json()

    # Creación de un registro asociado al usuario (esta comunicación ocurre en el frontend, por lo que se recibe el usuario y se envia el username)
    registro_data = {
        "nombre_archivo": "prueba.png",
        "probabilidad_sano": 0.80,
        "probabilidad_viral": 0.10,
        "probabilidad_bacteriana": 0.10,
        "estado": "DN.keras",
        "username": user["username"],
        "radiografia": "prueba"
    }
    registro_resp = client.post("/registros/", json=registro_data)
    assert registro_resp.status_code == 200
    registro = registro_resp.json()

    assert registro["nombre_archivo"] == "xray_lauratest.png"
    assert registro["username"] == user["username"]
