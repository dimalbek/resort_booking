from fastapi import APIRouter, Depends, HTTPException, status, Response
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext

from ..database.base import get_db
from ..database.models import User
from ..schemas.schemas import UserCreate, UserLogin, UserOut
from ..repositories.users import UsersRepository
from ..utils.security import get_admin_user, get_approved_user, get_current_user, create_access_token
from ..config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_DAYS

router = APIRouter(prefix="/auth", tags=["auth"])
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
users_repo = UsersRepository()



@router.post("/register", response_model=UserOut)
def register(user: UserCreate, db: Session = Depends(get_db)):
    db_user = users_repo.get_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = pwd_context.hash(user.password)
    user_in = UserCreate(
        email=user.email, password=hashed_password, is_admin=user.is_admin
    )
    user_return = users_repo.create(db, obj_in=user_in)
    return UserOut(
        id=user_return.id,
        email=user_return.email,
        is_admin=user_return.is_admin,
        is_approved=user_return.is_approved
    )


@router.post("/login")
def login(response: Response, user: UserLogin, db: Session = Depends(get_db)):
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
    return {"message": "Successfully logged in"}


@router.post("/logout")
def logout(response: Response):
    response.delete_cookie("access_token")
    return {"message": "Successfully logged out"}
