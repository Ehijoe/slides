from fastapi.testclient import TestClient

from backend.src.main import app
from backend.tests.fixtures import use_mock_db

client = TestClient(app)


def test_signup_create_user(use_mock_db):
    response = client.post(
        "/auth/signup/",
        json={"name": "Bazzi", "email": "bazz@gmail.com" , "password": "Dropthebazz", "password_confirm": "Dropthebazz"},
    )

    assert response.status_code == 200
    assert response.json()["name"]
    assert response.json()["email"]
    assert response.json()["id"]
    assert response.json()["is_active"] == False


def test_login_user(use_mock_db):
    response = client.post(
        "/auth/login/",
        json={"email": "bazz@gmail.com" , "password": "Dropthebazz"},
    )

    assert response.status_code == 400
    data = response.json()
    assert data["detail"] == "Account inactive"
