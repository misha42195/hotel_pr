from fastapi import Query, APIRouter, Body
from sqlalchemy import insert

from src.api.dependenies import PaginationDep
from src.schemas.hotels import Hotel
from src.database import async_session_maker
from src.models.hotels import HotelsOrm

router = APIRouter(prefix="/hotels", tags=["Отели"])

data_db = [
    {"id": 1, "title": "Sochi", "name": "sochi"},
    {"id": 2, "title": "Дубай", "name": "dubai"},
    {"id": 3, "title": "Мальдивы", "name": "maldivi"},
    {"id": 4, "title": "Геленджик", "name": "gelendzhik"},
    {"id": 5, "title": "Москва", "name": "moscow"},
    {"id": 6, "title": "Казань", "name": "kazan"},
    {"id": 7, "title": "Санкт-Петербург", "name": "spb"},
]


@router.get(
    "",
    summary="Получение всех отелей",
    description="Если не ввели параметры, то получаем список отелей"
    )
def get_hotels(
        data_hotel: PaginationDep,
        hotel_id: int | None = Query(default=None, description="ID отеля"),
        title: str | None = Query(default=None, description="Название отеля"),
):
    hotels_ = []
    for hotel in data_db:
        if hotel_id and hotel['id'] != hotel_id:
            continue
        if title and hotel['title'] != title:
            continue
        hotels_.append(hotel)
    if not data_hotel.page and not data_hotel.per_page:
        return hotels_
    return hotels_[data_hotel.per_page * (data_hotel.page - 1):][:data_hotel.per_page]


@router.delete(
    "/{hotels_id}",
    summary="Удаление отеля",
    description="Для удаления введите идентификатор отеля"
    )
def delete_hotel(hotel_id: int):
    global data_db
    data_db = [hotel for hotel in data_db if hotel_id != hotel['id']]
    return {'status': 'ok'}


@router.post(
    '',
    summary="Создание отеля"
    )
async def create_hotel(hotel_data: Hotel = Body(
    openapi_examples={
        "1": {
            "summary": "Сочи",
            "value": {
                "title": "Отель Сочи 5 звезд у моря",
                "location": "ул. Моря, 1",
            }
        },
        "2": {
            "summary": "Дубай",
            "value": {
                "title": "Отель Дубай У фонтана",
                "location": "ул. Шейха, 2",
            }
        }
    }
)
):
    async with async_session_maker() as session:
        add_hotel_stmt = insert(HotelsOrm).values(**hotel_data.model_dump())
        print(add_hotel_stmt)
        await session.execute(add_hotel_stmt)
        await session.commit()

    return {"status": "ok"}


@router.put(
    "/{hotels_id}",
    summary="Полное обновление данных",
    description="Для обновления необходимо ввести оба параметра \
            в теле запроса"
    )
def create_hotel_put(
        hotels_id: int,
        data_hotel: Hotel

):
    global data_db
    hotel = [hotel for hotel in data_db if hotel['id'] == hotels_id][0]
    hotel['title'] = data_hotel.title
    hotel['name'] = data_hotel.name
    return {"status": "ok"}


@router.patch(
    "/{hotels_id}",
    summary="Частичное обновление данных",
    description="Параметры title и name не обязательны, если передали, то меняем его значение"
    )
def create_hotel_patch(
        hotels_id: int,
        data_hotel: Hotel
):
    global data_db
    hotel = [hotel for hotel in data_db if hotel['id'] == hotels_id][0]
    if data_hotel.title:
        hotel['title'] = data_hotel.title
    if data_hotel.name:
        hotel['name'] = data_hotel.name
    return {"status": "ok"}
