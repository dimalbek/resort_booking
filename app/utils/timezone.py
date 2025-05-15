# app/utils/timezone.py
from datetime import datetime
import pytz

ALMATY_TZ = pytz.timezone("Asia/Almaty")


# ---------- helpers ---------------------------------------------------------

def now_almaty() -> datetime:
    """Текущее время в Алматы (aware)."""
    return datetime.now(ALMATY_TZ)


def date_almaty() -> datetime.date:
    """Текущая дата в Алматы."""
    return now_almaty().date()


def datetime_to_almaty(dt: datetime) -> datetime:
    """
    Приводит любой datetime к Asia/Almaty.
    Если был naive → делаем aware; если был aware → конвертируем.
    """
    if dt.tzinfo is None:
        return ALMATY_TZ.localize(dt)
    return dt.astimezone(ALMATY_TZ)


# ---------- UTC helpers -----------------------------------------------------

def now_utc() -> datetime:
    """Текущее UTC-время (aware)."""
    return datetime.utcnow().replace(tzinfo=pytz.UTC)


def to_utc(dt: datetime) -> datetime:
    """
    Любой datetime → Asia/Almaty (если naive) → UTC.
    Используем ПЕРЕД записью в Postgres, чтобы
    БД всегда хранила единый формат.                         #  <<<---
    """
    if dt.tzinfo is None:
        dt = ALMATY_TZ.localize(dt)
    return dt.astimezone(pytz.UTC)


def ensure_almaty(dt: datetime) -> datetime:
    """
    Делает объект timezone-aware (Asia/Almaty) для локального отображения.
    """
    if dt.tzinfo is None:
        return ALMATY_TZ.localize(dt)
    return dt.astimezone(ALMATY_TZ)
