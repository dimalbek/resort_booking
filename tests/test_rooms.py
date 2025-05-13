from datetime import datetime, timedelta
from fastapi.testclient import TestClient
from app.database.models import Room, User
import pytest


def test_get_available_rooms(client, db):
    # Создание тестового пользователя (владельца базы отдыха)
    user = User(
        email="owner@example.com",
        password="hashedpassword",
        is_admin=True,
        is_approved=True,
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    # Добавление комнаты
    room = Room(
        owner_id=user.id,
        room_number="101",
        max_guests=4,
        price_per_day=100,
        is_active=True,
    )
    db.add(room)
    db.commit()

    # Логинимся и получаем токен
    login_data = {"email": "owner@example.com", "password": "hashedpassword"}
    login_response = client.post("/auth/login", json=login_data)
    token = login_response.cookies.get("access_token")  # Получаем токен

    # Тестируем запрос для получения свободных комнат
    date_from = datetime.utcnow() + timedelta(days=1)
    date_to = date_from + timedelta(days=2)
    response = client.get(
        f"/rooms/available?owner_id={user.id}&date_from={date_from.isoformat()}&date_to={date_to.isoformat()}",
        cookies={"access_token": token},
    )

    assert response.status_code == 200
    assert len(response.json()) > 0
    assert response.json()[0]["room_number"] == "101"
