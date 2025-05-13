from datetime import datetime
from pydantic import BaseModel, EmailStr
from typing import Optional


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    is_admin: bool = False


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: int
    email: EmailStr
    is_admin: bool
    is_approved: bool


class RoomCreate(BaseModel):
    room_number: str
    max_guests: int
    price_per_day: int


class RoomOut(BaseModel):
    id: int
    room_number: str
    max_guests: int
    price_per_day: int
    is_active: bool


class BookingCreate(BaseModel):
    room_id: int
    room_number: int
    start: datetime
    end: datetime
    num_adults: int
    num_children: int
    num_infants: int


class BookingOut(BaseModel):
    id: int
    room_id: int
    room_number: int
    start: datetime
    end: datetime
    num_adults: int
    num_children: int
    num_infants: int
