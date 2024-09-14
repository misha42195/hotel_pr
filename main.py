from fastapi import FastAPI
import uvicorn

app = FastAPI()  # создаем экземпляр приложения

# импортируем объект router как router_hotels
from hotels import router as router_hotels

# добавляем в приложение роутер для отелей с префиксом /hotels
app.include_router(router_hotels)


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
