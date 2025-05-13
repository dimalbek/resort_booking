
from sqlalchemy.orm import Session
from ..database.models import User
from ..schemas.schemas import UserCreate, UserOut
from .base import BaseRepository
from typing import Optional
from fastapi.exceptions import HTTPException


class UsersRepository(BaseRepository[User, UserCreate, UserOut]):
    def __init__(self):
        super().__init__(User)

    def get_by_email(self, db: Session, email: str) -> Optional[User]:
        return db.query(self.model).filter(self.model.email == email).first()

    def approve_user(self, db: Session, user_id: int) -> User:
        user = self.get(db, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        user.is_approved = True
        db.commit()
        return user
    
    def disapprove_user(self, db: Session, user_id: int) -> User:
        user = self.get(db, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        user.is_approved = False
        db.commit()
        return user
    
    def reject_user(self, db: Session, user_id: int) -> None:
        user = self.get(db, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        db.delete(user)  # Удаляем пользователя из базы данных
        db.commit()
