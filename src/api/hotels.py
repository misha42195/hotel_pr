from fastapi import Query, APIRouter, Body
from sqlalchemy import insert, select

from src.api.dependenies import PaginationDep
from src.schemas.hotels import Hotel
from src.database import async_session_maker
from src.models.hotels import HotelsOrm
from src.database import engine
router = APIRouter(prefix="/hotels", tags=["Отели"])




@router.get(
    "",
    summary="Получение всех отелей",
    description="Если не ввели параметры, то получаем список отелей"
    )
async def get_hotels(
        data_hotel: PaginationDep,
        title: str | None = Query(default=None, description="Название отеля"),
        location: str | None = Query(default=None, description="Название отеля"),
):
    per_page = data_hotel.per_page or 5
    async with async_session_maker() as session:
        query = select(HotelsOrm)
        if title:
            query = query.filter(HotelsOrm.title.ilike(f"%{title}%"))
        if location:
            query = query.filter(HotelsOrm.title.ilike(f"%{location}%"))
        query = (
            query
            .limit(per_page)
            .offset(per_page * (data_hotel.page - 1))
        )
        result = await session.execute(query)
        result = result.scalars().all()
        return result


    # hotels_[data_hotel.per_page * (data_hotel.page - 1):][:data_hotel.per_page]


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
    summary="Создание отеля")
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
    })
):
    async with async_session_maker() as session:
        add_hotel_stmt = insert(HotelsOrm).values(**hotel_data.model_dump())
        print(add_hotel_stmt)
        print(add_hotel_stmt.compile(engine, compile_kwargs={"literal_binds":True}))
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
