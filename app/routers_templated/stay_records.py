from fastapi import APIRouter, Depends, HTTPException, Request, Form
from sqlalchemy.orm import Session
from datetime import datetime
from fastapi.templating import Jinja2Templates

from ..database.base import get_db
from ..database.models import User, StayRecord
from ..schemas.schemas import StayRecordCreate, StayRecordOut
from ..repositories.stay_records import StayRecordsRepository
from ..utils.security import get_current_user
from ..utils.timezone import now_almaty, now_utc, to_utc, datetime_to_almaty
import os


templates = Jinja2Templates(
    directory=os.path.join(os.path.dirname(__file__), "../templates")
)
router = APIRouter(prefix="/templated/stay_records", tags=["stay_records"])
stay_records_repo = StayRecordsRepository()


@router.get("/add")
async def get_add_stay_record_form(request: Request):
    return templates.TemplateResponse("add_stay_record_form.html", {"request": request})


@router.post("/add", response_model=StayRecordOut)
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
        raise HTTPException(
            status_code=403, detail="Недостаточно прав для добавления записи"
        )
    
    start_utc = to_utc(start)
    end_utc   = to_utc(end)

    stay_record = stay_records_repo.create_stay_record(
        db, current_user.id, start_utc, end_utc,
        num_adults, num_children, num_infants, name
    )

    return templates.TemplateResponse(
        "add_success.html",
        {
            "request": request,
            "start": start,
            "end": end,
            "num_adults": num_adults,
            "num_children": num_children,
            "num_infants": num_infants,
            "name": name,
        },
    )


# @router.get("/current_count", response_model=dict)
# async def get_current_count(
#     owner_id: int,
#     current_user: User = Depends(get_current_user),
#     db: Session = Depends(get_db),
# ):
#     if current_user.id != owner_id and not current_user.is_admin:
#         raise HTTPException(
#             status_code=403, detail="Недостаточно прав для получения данных"
#         )

#     now = now_almaty()
#     count = stay_records_repo.get_current_guests(db, owner_id, now)
#     return count


@router.get("/current_count")
async def current_count_page(
    request: Request,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if not current_user.is_approved:
        raise HTTPException(status_code=403, detail="Недостаточно прав для доступа")

    # now = now_almaty()
    now = now_utc()

    count = stay_records_repo.get_current_guests(db, current_user.id, now)

    return templates.TemplateResponse(
        "current_guests.html", {"request": request, "guests": count}
    )


@router.get("/users/{user_id}/stay_records")
async def get_user_stay_records(
    request: Request,
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.id != user_id or not current_user.is_approved:
        raise HTTPException(status_code=403, detail="Недостаточно прав для доступа")

    # now = now_almaty()
    now = now_utc()

    # Получаем все активные записи (где дата окончания больше или равна текущей)
    stay_records = (
        db.query(StayRecord)
        .filter(
            StayRecord.owner_id == user_id,
            StayRecord.end >= now,  # Фильтрация по дате окончания
        )
        .all()
    )

    for r in stay_records:
        r.start = datetime_to_almaty(r.start)
        r.end   = datetime_to_almaty(r.end)

    return templates.TemplateResponse(
        "user_stay_records.html",
        {"request": request, "stay_records": stay_records, "user": current_user},
    )


@router.post("/users/{user_id}/stay_records/{record_id}/delete")
async def delete_stay_record(
    request: Request,
    user_id: int,
    record_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.id != user_id or not current_user.is_approved:
        raise HTTPException(
            status_code=403, detail="Недостаточно прав для удаления записи"
        )

    stay_record = db.query(StayRecord).filter(StayRecord.id == record_id).first()

    if not stay_record:
        raise HTTPException(status_code=404, detail="Запись не найдена")

    db.delete(stay_record)
    db.commit()

    return templates.TemplateResponse(
        "delete_record_success.html",
        {"request": request, "message": f"Запись {stay_record.id} успешно удалена"},
    )



