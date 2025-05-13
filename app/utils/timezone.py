# app/utils/timezone.py
from datetime import datetime
import pytz

ALMATY_TZ = pytz.timezone('Asia/Almaty')

def now_almaty() -> datetime:
    """Возвращает текущее время в Алматы"""
    return datetime.now(ALMATY_TZ)

def date_almaty() -> datetime.date:
    """Возвращает текущую дату в Алматы"""
    return now_almaty().date()

def datetime_to_almaty(dt: datetime) -> datetime:
    """Конвертирует naive datetime в алматинское время"""
    if dt.tzinfo is None:
        return ALMATY_TZ.localize(dt)
    return dt.astimezone(ALMATY_TZ)