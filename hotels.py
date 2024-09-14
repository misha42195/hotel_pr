from fastapi import Query, APIRouter
from schemas.hotels import HotelPatch, HotelPUT

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

@router.get("",
            summary="Получение всех отелей",
            description="Если не ввели параметры, то получаем список отелей")
def get_hotels(

        id: int | None = Query(default=None, description="ID отеля"),
        title: str | None = Query(default=None, description="Название отеля"),
        page: int | None = Query(default=None, description="Номер страницы"),
        per_page: int | None = Query(default=None, description="Количество отелей на странице")

):

    hotels_ = []
    for hotel in data_db:
        if id and hotel['id'] != id:
            continue
        if title and hotel['title'] != title:
            continue
        hotels_.append(hotel)
    if not page and not per_page:
        return hotels_
    return hotels_[(page - 1) * per_page: page * per_page]


@router.delete("/{hotels_id}",
               summary="Удаление отеля",
               description="Для удаления введите идентификатор отеля")
def delete_hotel(hotel_id: int):
    global data_db
    data_db = [hotel for hotel in data_db if hotel_id != hotel['id']]
    return {'status': 'ok'}


@router.post('/',
             summary="Создание отеля")
def create_hotel(
        data_hotel: HotelPatch
):
    data_db.append(
        {'id': data_db[-1]['id'] + 1,
         'title': data_hotel.title,
         'name': data_hotel.name,
         }
    )
    return {"status": "ok"}


@router.put("/{hotels_id}",
            summary="Полное обновление данных",
            description="Для обновления необходимо ввести оба параметра \
            в теле запроса")
def create_hotel_put(
        hotels_id: int,
        data_hotel: HotelPUT

):
    global data_db
    hotel = [hotel for hotel in data_db if hotel['id'] == hotels_id][0]
    hotel['title'] = data_hotel.title
    hotel['name'] = data_hotel.name
    return {"status": "ok"}


@router.patch("/{hotels_id}",
              summary="Частичное обновление данных",
              description="Параметры title и name не обязательны, если передали, то меняем его значение")
def create_hotel_patch(
        hotels_id: int,
        data_hotel: HotelPatch
):
    global data_db
    hotel = [hotel for hotel in data_db if hotel['id'] == hotels_id][0]
    if data_hotel.title:
        hotel['title'] = data_hotel.title
    if data_hotel.name:
        hotel['name'] = data_hotel.name
    return {"status": "ok"}
