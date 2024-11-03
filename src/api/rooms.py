from datetime import date

from fastapi import APIRouter
from fastapi.params import Query

from api.dependenies import DBDep
from schemas.facilities import RoomFacilityAdd
from src.database import async_session_maker
from fastapi import Body

from src.repositories.rooms import RoomsRepository
from src.schemas.rooms import RoomResponseAdd, RoomAdd, RoomPatch, RoomPut

router = APIRouter(prefix="/hotels", tags=["Номера"])


@router.get("/{hotel_id/rooms}", summary="Получение номера")
async def get_rooms(
        hotel_id: int,
        db: DBDep,
        date_from: date = Query(example="2024-08-01"),
        date_to: date = Query(example="2024-08-10")

):
    room = await db.rooms.get_filtered_by_time(
        hotel_id=hotel_id,
        date_from=date_from,
        date_to=date_to)
    return {"status": "ok", "room": room}


@router.get("/{hotel_id}/rooms/{room_id}", summary="Получение номера")
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
        room_data: RoomResponseAdd = Body()
):
    _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
    room = await db.rooms.add(data=_room_data)

    room_facility_data = [RoomFacilityAdd(room_id=room.id, facility_id=f_id) for f_id in room_data.facilities_ids]
    await db.rooms_facilities.add_bulk(room_facility_data)
    await db.commit()

    return {"status": "ok", "room": room}


@router.put("/{hotel_id}/rooms/{room_id}", summary="Полное изменение номера")
async def full_edit_room(
        hotel_id: int,
        room_id: int,
        db: DBDep,
        room_data: RoomResponseAdd
):
    _room_data = RoomPut(hotel_id=hotel_id, **room_data.model_dump())
    await db.rooms.edite(
        data=_room_data,
        id=room_id)
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
