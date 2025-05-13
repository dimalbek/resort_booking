# tests/test_bookings.py
from datetime import datetime, timedelta
from fastapi.testclient import TestClient
from app.database.models import Booking, Room, User
import pytest
from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def test_create_booking(client, db):
    # Создание тестового пользователя
    user = User(
        email="user@example.com",
        password="hashedpassword",
        is_admin=False,
        is_approved=True,
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    # Хешируем пароль
    hashed_password = pwd_context.hash("password")

    # Создаем комнату
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
    login_data = {"email": "user@example.com", "password": "password"}
    login_response = client.post("/auth/login", json=login_data)
    token = login_response.cookies.get("access_token")  # Получаем токен

    # Создание бронирования
    date_from = datetime.utcnow() + timedelta(days=1)
    date_to = date_from + timedelta(days=2)
    booking_data = {
        "room_number": "101",
        "start": date_from.isoformat(),
        "end": date_to.isoformat(),
        "num_adults": 2,
        "num_children": 1,
        "num_infants": 0,
    }

    # Отправляем запрос с токеном в cookies
    response = client.post(
        "/bookings", json=booking_data, cookies={"access_token": token}
    )

    assert response.status_code == 200
    assert response.json()["room_number"] == "101"
