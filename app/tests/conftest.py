

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import Base, get_db
from main import app

# Banco SQLite em memória só para testes
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}  # necessário pro SQLite
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Fixture do banco — cria e destrói a cada teste
@pytest.fixture()
def db():
    Base.metadata.create_all(bind=engine)   # cria as tabelas
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)  # limpa tudo após o teste


# Fixture do cliente HTTP — substitui o get_db pelo banco de teste
@pytest.fixture()
def client(db):
    def override_get_db():
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()


# Fixture de usuário já criado no banco
@pytest.fixture()
def test_user(client):
    user_data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "senha123"
    }
    res = client.post("/users/", json=user_data)
    assert res.status_code == 201
    return res.json()


# Fixture de token autenticado
@pytest.fixture()
def token(client, test_user):
    res = client.post("/auth/login", data={
        "username": test_user["email"],
        "password": "senha123"
    })
    return res.json()["access_token"]


# Fixture de headers prontos pra usar
@pytest.fixture()
def authorized_client(client, token):
    client.headers = {**client.headers, "Authorization": f"Bearer {token}"}
    return client