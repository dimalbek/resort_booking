# from fastapi import APIRouter, Depends, HTTPException
# from sqlalchemy.orm import Session
# from datetime import datetime

# from ..database.base import get_db
# from ..database.models import User, Booking, Room
# from ..repositories.bookings import BookingsRepository
# from ..repositories.rooms import RoomsRepository
# from ..schemas.schemas import BookingCreate, BookingOut
# from ..utils.security import get_current_user
# from ..utils.timezone import now_almaty

# router = APIRouter(prefix="/bookings", tags=["bookings"])
# bookings_repo = BookingsRepository()
# rooms_repo = RoomsRepository()

# @router.post("", response_model=BookingOut)
# def create_booking(
#     booking: BookingCreate,
#     db: Session = Depends(get_db),
#     current_user: User = Depends(get_current_user)
# ):
#     # Проверяем, что комната с таким номером существует в базе отдыха пользователя
#     room = db.query(Room).filter(
#         Room.owner_id == current_user.id,
#         Room.room_number == booking.room_number
#     ).first()
    
#     if not room:
#         raise HTTPException(status_code=400, detail="Комната с таким номером не найдена")


#     room = rooms_repo.get(db, booking.room_id)
#     if not room:
#         raise HTTPException(status_code=400, detail="Превышена вместимость комнаты")
    
#     # проверяем доступность
#     available = rooms_repo.get_available(db, booking.start, booking.end, current_user.id,)
    
#     if not any(r.id == booking.room_id for r in available):
#         raise HTTPException(status_code=400, detail="Комната занята в это время")
    
#     booking_data = booking.dict()
#     booking_data["room_id"] = room.id
#     booking_data["user_id"] = current_user.id
#     booking_return = bookings_repo.create(db, obj_in=booking_data)
#     return booking_return

# @router.get("/available", response_model=list[BookingOut])
# def list_available(
#     start: datetime,
#     end: datetime,
#     total_guests: int,
#     current_user: User = Depends(get_current_user),
#     db: Session = Depends(get_db),
# ):
#     rooms = rooms_repo.get_available(db, start, end, current_user.id, total_guests)
#     # можно вернуть просто RoomOut, или для примера брони — пустой список
#     return rooms

# @router.get("/current-count", response_model=dict)
# def current_guest_count(
#     current_user: User = Depends(get_current_user),
#     db: Session = Depends(get_db)
# ):
#     now = now_almaty()
#     counts = bookings_repo.count_current_guests(db, current_user.id, now)
#     return counts
