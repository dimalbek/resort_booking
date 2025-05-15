import os
from dotenv import load_dotenv
from pathlib import Path

env_path = Path(__file__).resolve().parents[1] / '.env'
print(f".env !!!!!!!! {env_path}")

load_dotenv(dotenv_path=env_path)

POSTGRES_DB_URL = os.getenv("DATABASE_URL")
SQLALCHEMY_DATABASE_URL = POSTGRES_DB_URL.replace("postgres://", "postgresql://")

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_DAYS = int(os.getenv("ACCESS_TOKEN_EXPIRE_DAYS", 7))
