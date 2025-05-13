from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database.base import get_db
from ..database.models import User
from ..repositories.users import UsersRepository
from ..schemas.schemas import UserOut
from ..utils.security import get_current_user
from typing import List

router = APIRouter(prefix="/admin", tags=["admin"])
users_repo = UsersRepository()


@router.get("/users/pending", response_model=List[UserOut])
def get_pending_users(
    db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Admin access required")
    
    pending_users = db.query(User).filter(User.is_approved == False).all()
    return [
        UserOut(
            id=user.id,
            email=user.email,
            is_admin=user.is_admin,
            is_approved=user.is_approved
        )
        for user in pending_users
    ]


@router.post("/users/{user_id}/approve", response_model=UserOut)
def approve_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Admin access required")
    user = users_repo.approve_user(db, user_id)
    return UserOut(
        id=user.id,
        email=user.email,
        is_admin=user.is_admin,
        is_approved=user.is_approved
    )


@router.post("/users/{user_id}/reject", response_model=UserOut)
def reject_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Admin access required")
    user = users_repo.reject_user(db, user_id)
    return UserOut(
        id=user.id,
        email=user.email,
        is_admin=user.is_admin,
        is_approved=user.is_approved
    )
