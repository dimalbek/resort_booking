# app/routers_templated/rooms.py
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from typing import Optional, List
from datetime import datetime

from ..database.base import get_db
from ..database.models import User, Room
from ..repositories.rooms import RoomsRepository
from ..schemas.schemas import RoomOut
from ..utils.security import get_current_user
import os

templates = Jinja2Templates(directory=os.path.join(os.path.dirname(__file__), "templates"))

router = APIRouter(prefix="/templated/rooms", tags=["rooms"])
rooms_repo = RoomsRepository()

@router.get("/available")
async def get_available_rooms_form(request: Request):
    return templates.TemplateResponse("rooms_form.html", {"request": request})

@router.post("/available")
async def get_available_rooms(
    request: Request,
    date_from: datetime,
    date_to: datetime,
    max_guests: Optional[int] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    available_rooms = rooms_repo.get_available(db, date_from, date_to, current_user.id, max_guests)
    return templates.TemplateResponse("available_rooms.html", {
        "request": request,
        "rooms": available_rooms
    })
