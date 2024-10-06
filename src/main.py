import sys

from fastapi import FastAPI
import uvicorn


from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

app = FastAPI()  # создаем экземпляр приложения

# импортируем объект router как router_hotels
from src.api.hotels import router as router_hotels
from src.api.auth import router as user_router
from src.api.rooms import router as room_router
from src.config import settings


# добавляем в приложение роутер для отелей с префиксом /auth
app.include_router(user_router)

# добавляем в приложение роутер для отелей с префиксом /hotels
app.include_router(router_hotels)

# добавляем в приложение роутер для комнат с префиксом /hotels
app.include_router(room_router)


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
