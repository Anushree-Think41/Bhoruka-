from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database.db_handler import Base, get_db
from app.models.user_model import User
from app.services.auth_service import create_access_token
import pytest

# Setup a test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(name="session")
def session_fixture():
    # Create only the tables relevant to user tests
    User.__table__.create(bind=engine, checkfirst=True)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        User.__table__.drop(bind=engine, checkfirst=True)

@pytest.fixture(name="client")
def client_fixture(session):
    def override_get_db():
        yield session
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()

def test_create_user(client):
    response = client.post(
        "/users/",
        json={"email": "test@example.com", "password": "password123"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "test@example.com"
    assert "id" in data
    assert "last_login" in data

def test_create_existing_user(client):
    client.post(
        "/users/",
        json={"email": "test@example.com", "password": "password123"}
    )
    response = client.post(
        "/users/",
        json={"email": "test@example.com", "password": "password123"}
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Email already registered"

def test_login_for_access_token(client, session):
    # Create a user first
    client.post(
        "/users/",
        json={"email": "login@example.com", "password": "password123"}
    )
    
    response = client.post(
        "/users/token",
        data={"username": "login@example.com", "password": "password123"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_login_incorrect_password(client):
    client.post(
        "/users/",
        json={"email": "wrongpass@example.com", "password": "password123"}
    )
    response = client.post(
        "/users/token",
        data={"username": "wrongpass@example.com", "password": "wrongpassword"}
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Incorrect username or password"

def test_login_unregistered_email(client):
    response = client.post(
        "/users/token",
        data={"username": "unregistered@example.com", "password": "password123"}
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Incorrect username or password"

def test_read_users_me(client, session):
    # Create a user and get a token
    client.post(
        "/users/",
        json={"email": "me@example.com", "password": "password123"}
    )
    token_response = client.post(
        "/users/token",
        data={"username": "me@example.com", "password": "password123"}
    )
    access_token = token_response.json()["access_token"]

    response = client.get(
        "/users/me",
        headers={"Authorization": f"Bearer {access_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "me@example.com"
    assert "id" in data

def test_read_users_me_unauthorized(client):
    response = client.get("/users/me")
    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"

def test_read_user_by_id(client, session):
    # Create a user
    create_user_response = client.post(
        "/users/",
        json={"email": "idtest@example.com", "password": "password123"}
    )
    user_id = create_user_response.json()["id"]

    response = client.get(f"/users/{user_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "idtest@example.com"
    assert data["id"] == user_id

def test_read_user_by_invalid_id(client):
    response = client.get("/users/99999")
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"
