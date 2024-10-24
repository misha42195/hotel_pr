import asyncio
import sys

from fastapi import FastAPI
import uvicorn

from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

app = FastAPI()  # создаем экземпляр приложения

# импортируем объекты router
from src.api.hotels import router as router_hotels
from src.api.auth import router as router_user
from src.api.rooms import router as router_room
from src.api.bookings import router as router_booking
from src.api.facilities import router as router_facility

app.include_router(router_user)
app.include_router(router_hotels)
app.include_router(router_room)
app.include_router(router_booking)
app.include_router(router_facility)

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
