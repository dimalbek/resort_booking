from sqlalchemy.orm import Session
from ..database.models import Booking, Room
from ..schemas.schemas import BookingCreate, BookingOut
from .base import BaseRepository
from sqlalchemy import func
from datetime import datetime

class BookingsRepository(BaseRepository[Booking, BookingCreate, BookingOut]):
    def __init__(self):
        super().__init__(Booking)

    def count_current_guests(
        self,
        db: Session,
        owner_id: int,
        at_time: datetime
    ) -> dict[str, int]:
        # выбираем все активные в этот момент брони по владельцу
        q = (
            db.query(Booking)
            .join(Room, Booking.room_id == Room.id)
            .filter(
                Room.owner_id == owner_id,
                Booking.start <= at_time,
                Booking.end >= at_time,
            )
        )
        counts = {"adults": 0, "children": 0, "infants": 0}
        for b in q.all():
            counts["adults"] += b.num_adults
            counts["children"] += b.num_children
            counts["infants"] += b.num_infants
        return counts