from fastapi.testclient import TestClient

from src.main import app

client = TestClient(app)


def test_signup_create_user():
    response = client.post(
        "/auth/signup/",
        json={"name": "Bazz", "email": "bazz@gmail.com" , "password": "Dropthebazz", "password_confirm": "Dropthebazz"},
    )

    assert response.status_code == 200
    assert response.json()["name"]
    assert response.json()["email"]
    assert response.json()["id"]
    assert response.json()["is_active"] == False


def test_login_user():
    response = client.post(
        "/auth/login/",
        json={"email": "bazz@gmail.com" , "password": "Dropthebazz"},
    )

    assert response.status_code == 400