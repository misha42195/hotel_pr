from datetime import date

from fastapi import APIRouter
from fastapi.params import Query

from src.api.dependenies import DBDep
from src.schemas.facilities import RoomFacilityAdd
from src.schemas.rooms import RoomPatchRequest
from fastapi import Body

from src.schemas.rooms import RoomResponseAdd, RoomAdd, RoomPatch

router = APIRouter(prefix="/hotels", tags=["Номера"])


@router.get("/{hotel_id/rooms}", summary="Получение номеров")
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
    room = await db.rooms.get_one_or_none_with_rels(
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
    _room_data = RoomPatch(hotel_id=hotel_id, **room_data.model_dump())
    await db.rooms.edite(data=_room_data, id=room_id)

    await db.rooms_facilities.set_facilities(room_id=room_id, facilities_ids=room_data.facilities_ids)

    await db.commit()

    return {"status": "ok"}


@router.patch("/{hotel_id}/rooms/{room_id}", summary="Частичное обновление номера")
async def edit_room(
        hotel_id: int,
        room_id: int,
        db: DBDep,
        room_data: RoomPatchRequest
):
    _room_data_dict = room_data.model_dump(exclude_unset=True)
    _room_data = RoomPatch(hotel_id=hotel_id, **_room_data_dict)

    await db.rooms.edite(data=_room_data, id=room_id, hotel_id=hotel_id)
    if "facilities_ids" in _room_data_dict:
        await db.rooms_facilities.set_facilities(room_id=room_id, facilities_ids=_room_data_dict["facilities_ids"])

    await db.commit()

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
    return {"status": "ok"}
