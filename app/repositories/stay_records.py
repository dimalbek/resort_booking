from sqlalchemy.orm import Session
from ..database.models import StayRecord
from ..schemas.schemas import StayRecordCreate
from .base import BaseRepository
from datetime import datetime

class StayRecordsRepository(
    BaseRepository[StayRecord, StayRecordCreate, StayRecordCreate]
):
    def __init__(self):
        super().__init__(StayRecord)

    def get_current_guests(self, db: Session, owner_id: int, at_time: datetime):
        """Функция для подсчета количества людей на базе на указанное время"""
        records = (
            db.query(StayRecord)
            .filter(StayRecord.owner_id == owner_id)
            .filter(StayRecord.start <= at_time, StayRecord.end >= at_time)
            .all()
        )
        total_adults = sum(record.num_adults for record in records)
        total_children = sum(record.num_children for record in records)
        total_infants = sum(record.num_infants for record in records)
        return {
            "adults": total_adults,
            "children": total_children,
            "infants": total_infants,
        }

    def create_stay_record(
        self,
        db: Session,
        owner_id: int,
        start: datetime,
        end: datetime,
        num_adults: int,
        num_children: int,
        num_infants: int,
        name: str = None, 
        room_number: str | None = None,
    ):
        """Функция для создания записи о людях на базе"""
        stay_record = StayRecord(
            owner_id=owner_id,
            room_number  = room_number,
            start=start,
            end=end,
            num_adults=num_adults,
            num_children=num_children,
            num_infants=num_infants,
            name=name,
        )
        db.add(stay_record)
        db.commit()
        db.refresh(stay_record)
        return stay_record
