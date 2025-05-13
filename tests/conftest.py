import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database.base import Base, get_db
from app.database.models import User, Room, Booking
from fastapi.testclient import TestClient
from app.main import app

# Настройка тестовой БД
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_db.sqlite3"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="module")
def db():
    # Создаём таблицы
    Base.metadata.create_all(bind=engine)
    db_session = SessionLocal()
    yield db_session
    db_session.close()
    # Удаляем таблицы после тестов
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="module")
def client():
    client = TestClient(app)
    yield client
