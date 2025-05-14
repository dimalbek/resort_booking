from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from fastapi.templating import Jinja2Templates
from fastapi.responses import Response

from ..database.base import get_db
from ..database.models import User, StayRecord
from ..repositories.users import UsersRepository
from ..schemas.schemas import UserOut
from ..utils.security import get_current_user
from ..utils.timezone import now_almaty
from typing import List
import os


templates = Jinja2Templates(
    directory=os.path.join(os.path.dirname(__file__), "../templates")
)

router = APIRouter(prefix="/templated/admin", tags=["admin"])
users_repo = UsersRepository()


@router.get("/users/pending")
def get_pending_users(
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Admin access required")

    pending_users = db.query(User).filter(User.is_approved == False).all()
    return templates.TemplateResponse(
        "pending_users.html", {"request": request, "users": pending_users}
    )


@router.get("/users/approved")
async def get_approved_users(
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Admin access required")

    approved_users = db.query(User).filter(User.is_approved == True).all()
    return templates.TemplateResponse(
        "approved_users.html", {"request": request, "users": approved_users}
    )


@router.post("/users/{user_id}/approve", response_model=UserOut)
def approve_user(
    request: Request,
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Admin access required")
    user = users_repo.approve_user(db, user_id)
    return templates.TemplateResponse(
        "approve_user.html", {"request": request, "user": user}
    )


@router.post("/users/{user_id}/reject", response_model=UserOut)
def reject_user(
    request: Request,
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Admin access required")
    user = users_repo.reject_user(db, user_id)
    return templates.TemplateResponse(
        "reject_user.html", {"request": request, "user": user}
    )

@router.post("/users/{user_id}/revoke")
async def revoke_user_approval(
    request: Request,
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Admin access required")
    
    user = users_repo.disapprove_user(db, user_id)
    
    return templates.TemplateResponse("revoke_user.html", {
        "request": request, 
        "user": user,
        "message": "Права пользователя были отменены"
    })


@router.post("/cleanup")
async def delete_expired_records(
    request: Request,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Admin access required")
    # Удаляем все записи, которые уже закончились
    now = now_almaty()
    deleted_count = db.query(StayRecord).filter(StayRecord.end < now).delete()
    db.commit()
    return {"deleted_records": deleted_count}
