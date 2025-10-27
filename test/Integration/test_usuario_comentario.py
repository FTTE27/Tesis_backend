def test_usuario_crea_comentario(client):
    # Creación de un usuario
    user_data = {
        "nombre": "Juan",
        "username": "juan123",
        "password": "12345",
        "rol": "usuario",
        "disabled": False
    }
    user_resp = client.post("/usuarios/", json=user_data)
    assert user_resp.status_code == 200
    user = user_resp.json()

    # Creación de un comentario del usuario (esta comunicación ocurre en el frontend, por lo que se recibe el usuario y se envia el nombre)
    comentario_data = {
        "titulo": "Excelente modelo",
        "nombre": user["nombre"],
        "correo": "juan@example.com",
        "mensaje": "El sistema funciona muy bien."
    }
    comentario_resp = client.post("/comentarios/", json=comentario_data)
    assert comentario_resp.status_code == 200
    comentario = comentario_resp.json()

    # Verificar relación
    assert comentario["nombre"] == user["nombre"]
    assert comentario["titulo"] == "Excelente modelo"
