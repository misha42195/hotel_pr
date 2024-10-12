### Задание №11:
Функционал номеров
Необходимо создать API ручки для взаимодействия с номерами. 
По сути, нужны все те же самые ручки, что мы делали для отелей (см. скриншот).

Для этого нужны создать:
роутер и ручки
pydantic схемы
репозиторий

Давайте вынесем роутер с номерами в отдельный файл,
чтобы файл hotels.py не сильно распух 

Для начала нам необходимо создать ручку
```python
from fastapi import APIrouter

router = APIrouter(prefix="hotels",tags=["Номера"])

# в файле main.py импортируем router
from src.api.rooms import router as room_router

app.include_router(room_router)
```

Создадим схемы для работы методов получения, добавления, удаленияи обновления:

```python
from pydantic import BaseModel, ConfigDict

# схема для принятия запроса с определенными данными
# здесь нет поля hotel_id так как мы получаем значение при запросе
class RoomResponseAdd(BaseModel):
    title: str
    description: str
    price:int
    quantity: int

# схема, идентичная полям таблицы модели, кроме id
class RoomAdd(BaseModel):
    hotel_id: int
    title: str
    description: str
    price:int
    quantity: int


# схема для преобразования в объект room при получении данных из БД
class Room(RoomAdd):
    id: int
    
    model_config = ConfigDict(from_attributes=True)

# поля для изменения состояния объекта, кроме id
class RoomPatch(BaseModel):
    hotel_id: int | None = None
    title: str| None = None
    description: str| None = None
    price:int| None = None
    quantity: int | None = None

# поля для изменения состояния объекта, кроме id
class RoomPut(BaseModel):
    hotel_id: int
    title: str
    description: str
    price:int
    quantity: int
```

создадим ручку получения отеля, в качестве аргумента принимат два параметра:

1) hotel_id значение, по которому происходит фильтрация и находится определенный отел у которого хотим полцчить номер

2) room_id значение по которому фильтруем и находим номер по id, так как оно уникально

```python
@router.get("/{hotel_id}/rooms/{room_id}",summary="Получение отеля")
async def get_room(
    hotel_id: int,
    room_id: int,

):
    async with async_session_maker() as session:
        room =  await RoomsRepository(session).get_one_or_none(
            id=room_id,
            hotel_id=hotel_id)
        
        return {"status":"ok","room":room}
```

ручка для создания номеров, в качестве аргумента передаем значение
1)hotel_id, так как номера создаем для определенного отеля
2)room_data аргумент объекта схемы запроса, который содержит поля 
кроме hotel_id и id

```python
@router.post("/{hotel_id}/rooms/",summary="Создание номера")
async def create_room(
    hotel_id:int,
    room_data: RoomResponseAdd = Body()
    ):
    _room_data = RoomAdd(hotel_id=hotel_id,**room_data.model_dump())
    async with async_session_maker() as session:
        await RoomsRepository(session).add(
            data=_room_data)
        await session.commit()

    return {"stataus":"ok"}
    
```

По аналогии создаем другие ручки
ВЫВОД:
При создании ручки необходимо придерживатся REST-именования ручек
Создаем схемы для работы с входными данными, которые будут или менять или обновлять ручку