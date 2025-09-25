from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database.db_handler import Base, get_db
from app.models.user_model import User
from app.models.owner_model import Owner
from app.models.establishment_model import Establishment as DBEstablishment
import pytest

# Setup a test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(name="session")
def session_fixture():
    # Create only the tables relevant to owner tests
    User.__table__.create(bind=engine, checkfirst=True)
    Owner.__table__.create(bind=engine, checkfirst=True)
    # DBEstablishment.__table__.create(bind=engine, checkfirst=True) # Exclude Establishment due to ARRAY type issue with SQLite

    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        User.__table__.drop(bind=engine, checkfirst=True)
        Owner.__table__.drop(bind=engine, checkfirst=True)
        # DBEstablishment.__table__.drop(bind=engine, checkfirst=True)

@pytest.fixture(name="client")
def client_fixture(session):
    def override_get_db():
        yield session
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()

def test_create_owner(client):
    response = client.post(
        "/owners/",
        json={
            "owner_name": "Test Owner",
            "primary_phone": "+919876543210",
            "secondary_phone": "+919876543211",
            "email": "testowner@example.com"
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["owner_name"] == "Test Owner"
    assert data["primary_phone"] == "+919876543210"
    assert data["email"] == "testowner@example.com"
    assert "id" in data

def test_create_owner_existing_email(client):
    client.post(
        "/owners/",
        json={
            "owner_name": "Owner One",
            "primary_phone": "+911111111111",
            "email": "existing@example.com"
        }
    )
    response = client.post(
        "/owners/",
        json={
            "owner_name": "Owner Two",
            "primary_phone": "+912222222222",
            "email": "existing@example.com"
        }
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Email already registered"

def test_create_owner_existing_phone(client):
    client.post(
        "/owners/",
        json={
            "owner_name": "Owner Three",
            "primary_phone": "+913333333333",
            "email": "unique3@example.com"
        }
    )
    response = client.post(
        "/owners/",
        json={
            "owner_name": "Owner Four",
            "primary_phone": "+913333333333",
            "email": "unique4@example.com"
        }
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Primary phone already registered"

def test_read_owners(client):
    client.post(
        "/owners/",
        json={
            "owner_name": "Owner Five",
            "primary_phone": "+915555555555",
            "email": "owner5@example.com"
        }
    )
    client.post(
        "/owners/",
        json={
            "owner_name": "Owner Six",
            "primary_phone": "+916666666666",
            "email": "owner6@example.com"
        }
    )
    response = client.get("/owners/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 2 

def test_read_owners_with_skip_limit(client):
    for i in range(10):
        client.post(
            "/owners/",
            json={
                "owner_name": f"Owner {i}",
                "primary_phone": f"+\n9177777777{i}",
                "email": f"owner{i}@example.com"
            }
        )
    response = client.get("/owners/?skip=2&limit=5")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 5
    assert data[0]["owner_name"] == "Owner 2"

def test_read_owner_by_id(client):
    create_response = client.post(
        "/owners/",
        json={
            "owner_name": "Owner Seven",
            "primary_phone": "+917777777777",
            "email": "owner7@example.com"
        }
    )
    owner_id = create_response.json()["id"]

    response = client.get(f"/owners/{owner_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["owner_name"] == "Owner Seven"
    assert data["id"] == owner_id

def test_read_owner_by_invalid_id(client):
    response = client.get("/owners/99999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Owner not found"

def test_update_owner(client):
    create_response = client.post(
        "/owners/",
        json={
            "owner_name": "Owner Eight",
            "primary_phone": "+918888888888",
            "email": "owner8@example.com"
        }
    )
    owner_id = create_response.json()["id"]

    update_response = client.put(
        f"/owners/{owner_id}",
        json={
            "owner_name": "Updated Owner Eight",
            "primary_phone": "+918888888888",
            "secondary_phone": "+918888888889",
            "email": "updatedowner8@example.com"
        }
    )
    assert update_response.status_code == 200
    data = update_response.json()
    assert data["owner_name"] == "Updated Owner Eight"
    assert data["email"] == "updatedowner8@example.com"

def test_update_non_existent_owner(client):
    response = client.put(
        "/owners/99999",
        json={
            "owner_name": "Non Existent",
            "primary_phone": "+911234567890",
            "email": "nonexistent@example.com"
        }
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "Owner not found"

def test_delete_owner(client):
    create_response = client.post(
        "/owners/",
        json={
            "owner_name": "Owner Nine",
            "primary_phone": "+919999999999",
            "email": "owner9@example.com"
        }
    )
    owner_id = create_response.json()["id"]

    delete_response = client.delete(f"/owners/{owner_id}")
    assert delete_response.status_code == 204

    # Verify owner is deleted
    get_response = client.get(f"/owners/{owner_id}")
    assert get_response.status_code == 404

def test_delete_non_existent_owner(client):
    response = client.delete("/owners/99999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Owner not found"

# Test for establishments for owner - requires Establishment table
# This test will be skipped for now due to SQLite ARRAY type issue
# def test_read_establishments_for_owner(client, session):
#     # Create an owner
#     owner_response = client.post(
#         "/owners/",
#         json={
#             "owner_name": "Owner With Establishments",
#             "primary_phone": "+911000000000",
#             "email": "ownerwithest@example.com"
#         }
#     )
#     owner_id = owner_response.json()["id"]

#     # Create an establishment for the owner (this part would need to be mocked or use a different DB)
#     # For now, we'll just test the 404 case if no establishments are found

#     response = client.get(f"/owners/{owner_id}/establishments")
#     assert response.status_code == 404
#     assert response.json()["detail"] == "No establishments found for this owner"

# def test_read_establishments_for_invalid_owner(client):
#     response = client.get("/owners/99999/establishments")
#     assert response.status_code == 404
#     assert response.json()["detail"] == "Owner not found"
