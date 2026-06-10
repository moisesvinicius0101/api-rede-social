


def test_register(client):
    response = client.post(
        "/auth/register",
        json={
            "username": "Jhone",
            "email": "jhone123@gmail.com",
            "password": "jhone@123456"
        }
    )

    assert response.status_code == 201

    data = response.json()

    assert "access_token" in data
    assert isinstance(data["access_token"], str)
    assert data["token_type"] == "bearer"

    assert "detail" not in data
    

def test_register_duplicate_email(client, test_user):
    response = client.post(
        "/auth/register",
        json={
            "username": "outro_usuario",
            "email": test_user["email"],
            "password": "123456"
        }
    )

    assert response.status_code == 400

    data = response.json()

    assert data["detail"] == "Este e-mail já está em uso."
    
def test_register_duplicate_username(client, test_user):
    response = client.post(
        "/auth/register",
        json={
            "username": test_user["username"],
            "email": "novo@gmail.com",
            "password": "123456"
        }
    )

    assert response.status_code == 400

    data = response.json()

    assert data["detail"] == "Este nome de usuário já está em uso."
    
def test_register_invalid_email(client):
    response = client.post(
        "/auth/register",
        json={
            "username": "Jhone",
            "email": "email_invalido",
            "password": "123456"
        }
    )

    assert response.status_code == 422
    
def test_register_short_password(client):
    response = client.post(
        "/auth/register",
        json={
            "username": "Jhone",
            "email": "jhone@gmail.com",
            "password": "123"
        }
    )

    assert response.status_code == 422
    
    
def test_login(client, test_user):
    response = client.post(
        "/auth/login",
        json={
            "email": test_user["email"],
            "password": test_user["password"]
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert "access_token" in data
    assert isinstance(data["access_token"], str)

    assert data["token_type"] == "bearer"
    
def test_login_invalid_credentials(client):
    response = client.post(
        "/auth/login",
        json={
            "email": "naoexiste@gmail.com",
            "password": "senha_errada"
        }
    )

    assert response.status_code == 401

    data = response.json()

    assert data["detail"] == "E-mail ou senha incorretos."