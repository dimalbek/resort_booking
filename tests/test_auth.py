# tests/test_auth.py
from fastapi.testclient import TestClient
from app.database.models import User
import pytest
from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def test_register(client, db):
    user_data = {
        "email": "testuser@example.com",
        "password": "password",
        "is_admin": False,
    }

    response = client.post("/auth/register", json=user_data)
    assert response.status_code == 200
    assert response.json()["email"] == "testuser@example.com"


def test_login(client, db):
    hashed_password = pwd_context.hash("hashedpassword")
    user = User(
        email="loginuser@example.com",
        password=hashed_password,
        is_admin=False,
        is_approved=True,
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    login_data = {"email": "loginuser@example.com", "password": "hashedpassword"}

    response = client.post("/auth/login", json=login_data)
    assert response.status_code == 200
    assert "access_token" in response.cookies
