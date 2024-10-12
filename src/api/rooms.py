from fastapi import APIRouter

from api.dependenies import DBDep
from src.database import async_session_maker
from fastapi import Body

from src.repositories.rooms import RoomsRepository
from src.schemas.rooms import RoomResponseAdd, RoomAdd, RoomPatch, RoomPut

router = APIRouter(prefix="/hotels", tags=["Номера"])


@router.get("/{hotel_id}/rooms/{room_id}", summary="Получение отеля")
async def get_room(
        hotel_id: int,
        room_id: int,
        db: DBDep,

):
    room = await db.rooms.get_one_or_none(
        id=room_id,
        hotel_id=hotel_id)
    return {"status": "ok", "room": room}


@router.post("/{hotel_id}/rooms/", summary="Создание номера")
async def create_room(
        hotel_id: int,
        db: DBDep,
        room_data: RoomResponseAdd = Body(openapi_examples={
            "1": {
                "summary": "Стандарт",
                "value": {
                    "hotel_id": 54,
                    "title": "Сатндартный номер",
                    "description": "Стандартный двухместный номер",
                    "price": 4000,
                    "quantity": 20,
                }
            },
            "2": {
                "summary": "Премиум",
                "value": {
                    "hotel_id": 54,
                    "title": "Премиму номер",
                    "description": "Премиальный номер",
                    "price": 10000,
                    "quantity": 3,
                }
            }
        }
        )):
    _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
    await db.rooms.add(data=_room_data)
    await db.rooms.commit()

    return {"stataus": "ok"}


@router.put("/{hotel_id}/rooms/{room_id}", summary="Полное изменение номера")
async def full_edit_room(
        hotel_id: int,
        roon_id: int,
        db: DBDep,
        room_data: RoomResponseAdd
):
    _room_data = RoomPut(hotel_id=hotel_id, **room_data.model_dump())
    await db.rooms.edite(
        data=_room_data,
        id=roon_id)
    await db.rooms.commit()

    return {"status": "ok"}


@router.patch("/{hote_id}/rooms/{room_id}", summary="Частичное обновление номера")
async def edir_room(
        hotel_id: int,
        room_id: int,
        db: DBDep,
        room_data: RoomResponseAdd
):
    _room_data = RoomPatch(hotel_id=hotel_id, **room_data.model_dump())
    await db.rooms.edite(
        data=_room_data,
        id=room_id)
    await db.rooms.commit()

    return {"status": "ok"}


@router.delete("/{hotel_id}/rooms/{room_id}", summary="Удаление отеля")
async def delete_room(
        hotel_id: int,
        room_id: int,
        db: DBDep,
):
    await db.rooms.delete(
        id=room_id,
        hotel_id=hotel_id)
    await db.rooms.commit()
    return {"ststus": "ok"}
