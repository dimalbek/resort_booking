from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from fastapi import Request
import os
from .database.models import User
from .utils.security import get_current_user_first_visit

from .routers import auth, admin
# from .routers_templated import rooms as templated_rooms
from .routers_templated import admin as templated_admin
from .routers_templated import auth as templated_auth
from .routers_templated import stay_records as templated_stay_records
# from .routers_templated import bookings as templated_bookings

from fastapi.staticfiles import StaticFiles


app = FastAPI()

# Настроим middleware для CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключаем Jinja2 для использования шаблонов
templates = Jinja2Templates(directory=os.path.join(os.path.dirname(__file__), "templates"))

# Подключаем папку для статики
app.mount("/static", StaticFiles(directory="static"), name="static")


# Включаем роутеры
app.include_router(auth.router)
app.include_router(admin.router)
# app.include_router(rooms.router)
# app.include_router(bookings.router)

app.include_router(templated_auth.router)
app.include_router(templated_admin.router)
app.include_router(templated_stay_records.router)
# app.include_router(templated_rooms.router)
# app.include_router(templated_bookings.router)

@app.get("/")
def read_root():
    return {"message": "Resort Room Booking API"}

# Пример для шаблонов (например, главная страница)
@app.get("/templated/")
async def homepage(request: Request,  current_user: User | None = Depends(get_current_user_first_visit)):
    if not current_user:
        return templates.TemplateResponse("index.html", {"request": request})

    return templates.TemplateResponse("index.html", {"request": request, "user": current_user})


@app.get("/healthcheck")
def health_check():
    return {"status": "ok"}