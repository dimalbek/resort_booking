# from sqlalchemy.orm import Session
# from datetime import date, datetime
# from ..database.models import Room, Booking
# from ..schemas.schemas import RoomCreate, RoomOut
# from .base import BaseRepository
# from typing import Optional, List


# class RoomsRepository(BaseRepository[Room, RoomCreate, RoomOut]):
#     def __init__(self):
#         super().__init__(Room)

#     def get_available(
#         self,
#         db: Session,
#         start: datetime,
#         end: datetime,
#         owner_id: int,
#         total_guests: Optional[int] = None,
#     ) -> List[Room]:
#         query = db.query(Room).filter(
#             Room.owner_id == owner_id,
#             Room.is_active == True,
#             ~Room.bookings.any((Booking.start <= end) & (Booking.end >= start)),
#         )
#         if total_guests:
#             query = query.filter(Room.max_guests >= total_guests)
#         return query.all()
