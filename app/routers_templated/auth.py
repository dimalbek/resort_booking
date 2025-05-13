# app/routers_templated/auth.py
from fastapi import APIRouter, Depends, HTTPException, Request, Form, Response
from sqlalchemy.orm import Session
from fastapi.templating import Jinja2Templates
from ..database.base import get_db
from ..schemas.schemas import UserCreate, UserLogin, UserOut
from ..repositories.users import UsersRepository
from ..utils.security import create_access_token
from ..config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_DAYS
from passlib.context import CryptContext
import os


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
templates = Jinja2Templates(directory=os.path.join(os.path.dirname(__file__), "../templates"))

router = APIRouter(prefix="/templated/auth", tags=["auth"])
users_repo = UsersRepository()


@router.get("/register")
async def get_register_form(request: Request):
    return templates.TemplateResponse("register_form.html", {"request": request})


@router.post("/register", response_model=UserOut)
async def register(request: Request, user: UserCreate, db: Session = Depends(get_db)):
    db_user = users_repo.get_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = pwd_context.hash(user.password)
    user_in = UserCreate(
        email=user.email, password=hashed_password, is_admin=user.is_admin
    )
    user_return = users_repo.create(db, obj_in=user_in)
    return templates.TemplateResponse(
        "register_success.html", {"request": request, "user": user_return}
    )


@router.get("/login")
async def get_login_form(request: Request):
    return templates.TemplateResponse("login_form.html", {"request": request})


@router.post("/login")
async def login(request: Request, response: Response, user: UserLogin, db: Session = Depends(get_db)):
    db_user = users_repo.get_by_email(db, email=user.email)
    if not db_user or not pwd_context.verify(user.password, db_user.password):
        raise HTTPException(status_code=400, detail="Incorrect email or password")

    token = create_access_token(db_user.id)
    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        max_age=ACCESS_TOKEN_EXPIRE_DAYS * 7 * 3600,
        secure=True,
    )
    return templates.TemplateResponse(
        "login_success.html", {"request": request, "message": "Successfully logged in"}
    )
