from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_create_user():

    response = client.post(
        "/users",
        json={
            "username": "alice",
            "email": "alice@example.com",
            "password": "Password123!"
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["username"] == "alice"
    assert data["email"] == "alice@example.com"


def test_duplicate_username():

    response = client.post(
        "/users",
        json={
            "username": "alice",
            "email": "alice2@example.com",
            "password": "Password123!"
        },
    )

    assert response.status_code == 409


def test_get_user():

    response = client.get("/users/alice")

    assert response.status_code == 200

    data = response.json()

    assert data["username"] == "alice"