from fastapi import Query, APIRouter, Body

from src.api.dependenies import PaginationDep
from src.schemas.hotels import Hotel, HotelPATCH
from src.database import async_session_maker
from src.repositories.hotels import HotelsRepository
from src.schemas.hotels import HotelAdd
from src.api.dependenies import DBDep

router = APIRouter(prefix="/hotels", tags=["Отели"])


@router.get(
    "",
    summary="Получение всех отелей",
    description="Если не ввели параметры, то получаем список отелей"
)
async def get_hotels(
        data_hotel: PaginationDep,
        db: DBDep,
        title: str | None = Query(default=None, description="Название отеля"),
        location: str | None = Query(default=None, description="Название отеля"),
):
    per_page = data_hotel.per_page or 5
    # async with async_session_maker() as session:
    return await db.hotels.get_all(
        title=title,
        location=location,
        limit=per_page,
        offset=(per_page * (data_hotel.page - 1))
    )


@router.delete(
    "/{hotels_id}",
    summary="Удаление отеля",
    description="Для удаления введите идентификатор отеля"
)
async def delete_hotel(
        hotel_id: int,
        db: DBDep
):
    await db.hotels.delete(id=hotel_id)
    await db.commit()
    return {'status': 'ok'}


@router.post("", summary="Создание отеля")
async def create_hotel(
        db: DBDep,
        hotel_data: HotelAdd = Body(openapi_examples={
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
        })
):
    hotel = await db.hotels.add(hotel_data)
    await db.commit()

    return {"status": "ok", "data": hotel}


@router.get("/{hotel_id/}", summary="Получение одного отеля по ID")
async def get_hotel(
        hotel_id: int,
        db: DBDep
):
    hotel = await db.hotels.get_one_or_none(id=hotel_id)
    return {"status": "ok", "data": hotel}


@router.put(
    "/{hotels_id}",
    summary="Полное обновление данных",
    description="Для обновления необходимо ввести оба параметра \
            в теле запроса"
)
async def create_hotel_put(
        hotels_id: int,
        hotel_data: HotelAdd,
        db: DBDep
):
    await db.hotels.edite(hotel_data, id=hotels_id)
    await db.commit()

    return {"status": "ok"}


@router.patch(
    "/{hotels_id}",
    summary="Частичное обновление данных",
    description="Параметры title и name не обязательны, если передали, то меняем его значение"
)
async def create_hotel_patch(
        hotels_id: int,
        data_hotel: HotelPATCH,
        db:DBDep
):
    await db.hotels.edite(data_hotel, id=hotels_id)
    await db.commit()

    return {"status": "ok"}
