import sys

from fastapi import FastAPI
import uvicorn


from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

app = FastAPI()  # создаем экземпляр приложения

# импортируем объект router как router_hotels
from src.api.hotels import router as router_hotels
from src.config import settings

print(f"{settings.DB_URL}")

# добавляем в приложение роутер для отелей с префиксом /hotels
app.include_router(router_hotels)



if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
