from sqlalchemy import Column, Integer, String, Boolean, Date, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from .base import Base
from datetime import datetime


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    is_admin = Column(Boolean, default=False)
    is_approved = Column(Boolean, default=False)

    stay_records = relationship("StayRecord", back_populates="owner")


class StayRecord(Base):
    __tablename__ = "stay_records"

    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(
        Integer, ForeignKey("users.id")
    )  # Ссылка на владельца базы отдыха
    start = Column(DateTime, nullable=False)
    end = Column(DateTime, nullable=False)
    num_adults = Column(Integer, nullable=False, default=0)
    num_children = Column(Integer, nullable=False, default=0)
    num_infants = Column(Integer, nullable=False, default=0)
    name = Column(String, nullable=True)


    owner = relationship("User", back_populates="stay_records")


# class Room(Base):
#     __tablename__ = "rooms"

#     id = Column(Integer, primary_key=True, index=True)
#     owner_id = Column(Integer, ForeignKey("users.id"))
#     room_number = Column(String, nullable=False)  # Номер комнаты
#     max_guests = Column(Integer, nullable=False)
#     price_per_day = Column(Integer, nullable=False)
#     is_active = Column(Boolean, default=True)

#     owner = relationship("User", back_populates="rooms")
#     bookings = relationship("Booking", back_populates="room")


# class Booking(Base):
#     __tablename__ = "bookings"

#     id = Column(Integer, primary_key=True, index=True)
#     room_id = Column(Integer, ForeignKey("rooms.id"), nullable=False)
#     user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
#     start = Column(DateTime, nullable=False)
#     end = Column(DateTime, nullable=False)
#     num_adults = Column(Integer, nullable=False, default=1)
#     num_children = Column(Integer, nullable=False, default=0)
#     num_infants = Column(Integer, nullable=False, default=0)

#     room = relationship("Room", back_populates="bookings")
#     user = relationship("User", back_populates="bookings")
