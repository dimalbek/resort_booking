from datetime import datetime
import os
from typing import List

import pytz
from fastapi import (
    APIRouter, Depends, HTTPException,
    Request, Form
)
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from ..database.base import get_db
from ..database.models import User, StayRecord
from ..repositories.stay_records import StayRecordsRepository
from ..utils.security import get_current_user
from ..utils.timezone import (
    now_almaty, now_utc, to_utc,
    datetime_to_almaty
)

# ---------------------------------------------------------------------------

templates = Jinja2Templates(
    directory=os.path.join(os.path.dirname(__file__), "../templates")
)
templates.env.globals["pytz"] = pytz

router = APIRouter(prefix="/templated/stay_records", tags=["stay_records"])
stay_records_repo = StayRecordsRepository()

# ---------------------------------------------------------------------------

@router.get("/add")
async def get_add_stay_record_form(request: Request):
    return templates.TemplateResponse(
        "add_stay_record_form.html",
        {"request": request}
    )


@router.post("/add")
async def add_stay_record(
    request: Request,
    name: str = Form(...),
    start: datetime = Form(...),
    end: datetime = Form(...),
    num_adults: int = Form(...),
    num_children: int = Form(...),
    num_infants: int = Form(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if not current_user.is_approved:
        raise HTTPException(status_code=403,
                            detail="Недостаточно прав для добавления записи")

    start_utc = to_utc(start)
    end_utc   = to_utc(end)

    stay_records_repo.create_stay_record(           #  <<<---
        db, current_user.id, start_utc, end_utc,
        num_adults, num_children, num_infants, name
    )

    return templates.TemplateResponse(
        "add_success.html",
        {
            "request": request,
            "start": start,       # показываем в Алмате
            "end":   end,
            "num_adults": num_adults,
            "num_children": num_children,
            "num_infants": num_infants,
            "name": name,
        },
    )

# ---------------------------------------------------------------------------

@router.get("/current_count")
async def current_count_page(
    request: Request,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if not current_user.is_approved:
        raise HTTPException(status_code=403, detail="Недостаточно прав для доступа")

    now = now_utc()                                # всегда UTC           #  <<<---
    counts = stay_records_repo.get_current_guests(db, current_user.id, now)

    return templates.TemplateResponse(
        "current_guests.html",
        {
            "request": request,
            "guests": counts,
            "now": datetime_to_almaty(now)          # выводим локально
        }
    )

# ---------------------------------------------------------------------------

@router.get("/guest_count")
async def guest_count_form(request: Request):
    return templates.TemplateResponse("guest_count_form.html",
                                      {"request": request})


@router.post("/guest_count")
async def guest_count_result(
    request: Request,
    at: datetime = Form(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if not current_user.is_approved:
        raise HTTPException(status_code=403, detail="Недостаточно прав")

    at_utc = to_utc(at)
    counts = stay_records_repo.get_current_guests(db, current_user.id, at_utc)

    return templates.TemplateResponse(
        "guest_count_result.html",
        {
            "request": request,
            "at": datetime_to_almaty(at_utc),        #  <<<---
            "counts": counts
        }
    )

# ---------------------------------------------------------------------------

@router.get("/users/{user_id}/stay_records")
async def get_user_stay_records(
    request: Request,
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.id != user_id or not current_user.is_approved:
        raise HTTPException(status_code=403, detail="Недостаточно прав для доступа")

    now = now_utc()

    raw_records: List[StayRecord] = (
        db.query(StayRecord)
        .filter(StayRecord.owner_id == user_id,
                StayRecord.end >= now)
        .all()
    )

    # НЕ мутируем ORM, делаем представление              #  <<<---
    stay_records = [
        {
            "id": r.id,
            "name": r.name,
            "start_local": datetime_to_almaty(r.start),
            "end_local":   datetime_to_almaty(r.end),
            "num_adults":   r.num_adults,
            "num_children": r.num_children,
            "num_infants":  r.num_infants,
        }
        for r in raw_records
    ]

    return templates.TemplateResponse(
        "user_stay_records.html",
        {"request": request, "stay_records": stay_records, "user": current_user},
    )

# ---------------------------------------------------------------------------

@router.post("/users/{user_id}/stay_records/{record_id}/delete")
async def delete_stay_record(
    request: Request,
    user_id: int,
    record_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.id != user_id or not current_user.is_approved:
        raise HTTPException(status_code=403, detail="Недостаточно прав для удаления записи")

    record = db.query(StayRecord).filter(StayRecord.id == record_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="Запись не найдена")

    db.delete(record)
    db.commit()

    return templates.TemplateResponse(
        "delete_record_success.html",
        {"request": request, "message": f"Запись {record.id} успешно удалена"},
    )

# ---------------------------------------------------------------------------

@router.get("/users/{user_id}/stay_records/{record_id}/edit")
async def edit_stay_record_form(
    request: Request,
    user_id: int,
    record_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.id != user_id or not current_user.is_approved:
        raise HTTPException(status_code=403, detail="Недостаточно прав")

    record = db.query(StayRecord).filter(StayRecord.id == record_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="Запись не найдена")

    view_record = {                               #  <<<---
        "id": record.id,
        "name": record.name,
        "start_local": datetime_to_almaty(record.start),
        "end_local":   datetime_to_almaty(record.end),
        "num_adults":   record.num_adults,
        "num_children": record.num_children,
        "num_infants":  record.num_infants,
    }

    return templates.TemplateResponse(
        "edit_stay_record_form.html",
        {"request": request, "record": view_record, "user_id": current_user.id   }
    )

# ---------------------------------------------------------------------------

@router.post("/users/{user_id}/stay_records/{record_id}/update")
async def update_stay_record(
    request: Request,
    user_id: int,
    record_id: int,
    name: str = Form(...),
    start: datetime = Form(...),
    end: datetime = Form(...),
    num_adults: int = Form(...),
    num_children: int = Form(...),
    num_infants: int = Form(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if current_user.id != user_id or not current_user.is_approved:
        raise HTTPException(status_code=403, detail="Недостаточно прав")

    if end <= start:                               #  <<<---
        raise HTTPException(status_code=400,
                            detail="Дата конца должна быть позже начала")

    record = db.query(StayRecord).filter(StayRecord.id == record_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="Запись не найдена")

    record.name         = name
    record.start        = to_utc(start)
    record.end          = to_utc(end)
    record.num_adults   = num_adults
    record.num_children = num_children
    record.num_infants  = num_infants

    db.commit()
    db.refresh(record)

    return templates.TemplateResponse(
        "edit_success.html",
        {"request": request,
         "record": {
             "name": name,
             "start": datetime_to_almaty(start),
             "end":   datetime_to_almaty(end)
         }}
    )
