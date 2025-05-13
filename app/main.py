from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from fastapi import Request
import os

from .routers import auth, admin, rooms, bookings
from .routers_templated import rooms as templated_rooms
from .routers_templated import admin as templated_admin
from .routers_templated import auth as templated_auth
from .routers_templated import bookings as templated_bookings


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

# Включаем роутеры
app.include_router(auth.router)
app.include_router(admin.router)
app.include_router(rooms.router)
app.include_router(bookings.router)

app.include_router(templated_auth.router)
app.include_router(templated_admin.router)
app.include_router(templated_rooms.router)
app.include_router(templated_bookings.router)

@app.get("/")
def read_root():
    return {"message": "Resort Room Booking API"}

# Пример для шаблонов (например, главная страница)
@app.get("/templated/")
async def homepage(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

