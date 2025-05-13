from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import date

from ..database.base import get_db
from ..database.models import User, Room
from ..repositories.rooms import RoomsRepository
from ..schemas.schemas import RoomCreate, RoomOut
from ..utils.security import get_current_user
from typing import Optional, List

router = APIRouter(prefix="/rooms", tags=["rooms"])
rooms_repo = RoomsRepository()

@router.post("", response_model=RoomOut)
def create_room(
    room: RoomCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not current_user.is_approved:
        raise HTTPException(status_code=403, detail="Account not approved")
    
    room_data = room.dict()
    room_data["owner_id"] = current_user.id
    room_return = rooms_repo.create(db, obj_in=room_data)
    return RoomOut(
        id = room_return.id,
        max_guests = room_return.max_guests,
        price_per_day = room_return.price_per_day,
        is_active = room_return.is_active
    )

@router.get("/available", response_model=List[RoomOut])
def get_available_rooms(
    date_from: date,
    date_to: date,
    max_guests: Optional[int] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    available_rooms = rooms_repo.get_available(db, date_from, date_to, current_user.id, max_guests)
    return [
        RoomOut(
            id = room_return.id,
            room_number=room_return.room_number,
            max_guests = room_return.max_guests,
            price_per_day = room_return.price_per_day,
            is_active = room_return.is_active
        )
        for room_return in available_rooms
    ]