# app/routers_templated/bookings.py
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from datetime import datetime

from ..database.base import get_db
from ..database.models import User, Booking, Room
from ..repositories.bookings import BookingsRepository
from ..repositories.rooms import RoomsRepository
from ..schemas.schemas import BookingCreate, BookingOut
from ..utils.security import get_current_user
from ..utils.timezone import now_almaty
import os

templates = Jinja2Templates(directory=os.path.join(os.path.dirname(__file__), "templates"))

router = APIRouter(prefix="/templated/bookings", tags=["bookings"])
bookings_repo = BookingsRepository()
rooms_repo = RoomsRepository()

@router.post("", response_model=BookingOut)
def create_booking(
    request: Request,
    booking: BookingCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    room = db.query(Room).filter(
        Room.owner_id == current_user.id,
        Room.room_number == booking.room_number
    ).first()
    
    if not room:
        raise HTTPException(status_code=400, detail="Комната с таким номером не найдена")

    room = rooms_repo.get(db, booking.room_id)
    if not room:
        raise HTTPException(status_code=400, detail="Превышена вместимость комнаты")
    
    available = rooms_repo.get_available(db, booking.start, booking.end, current_user.id,)
    
    if not any(r.id == booking.room_id for r in available):
        raise HTTPException(status_code=400, detail="Комната занята в это время")
    
    booking_data = booking.dict()
    booking_data["room_id"] = room.id
    booking_data["user_id"] = current_user.id
    booking_return = bookings_repo.create(db, obj_in=booking_data)
    return templates.TemplateResponse("booking_success.html", {
        "request": request,
        "booking": booking_return
    })
