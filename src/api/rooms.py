from fastapi import APIRouter

from src.database import async_session_maker
from fastapi import Body

from src.repositories.rooms import RoomsRepository
from src.schemas.rooms import RoomResponseAdd, RoomAdd, RoomPatch, RoomPut


router = APIRouter(prefix="/hotels",tags=["Номера"])

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

@router.put("/{hotel_id}/rooms/{room_id}",summary="Полное изменение номера")
async def full_edit_room(
    hotel_id:int,
    roon_id:int,
    room_data:RoomResponseAdd
):
    _room_data = RoomPut(hotel_id=hotel_id,**room_data.model_dump())
    async with async_session_maker() as session:
        await RoomsRepository(session).edite(
            data=_room_data,
            id=roon_id)
        await session.commit()

    return {"ststus":"ok"}

@router.patch("/{hote_id}/rooms/{room_id}",summary="Частичное обновление номера")
async def edir_room(
    hotel_id:int,
    room_id:int,
    room_data: RoomResponseAdd
):
    _room_data = RoomPatch(hotel_id=hotel_id,**room_data.model_dump())
    async with async_session_maker() as session:
        await RoomsRepository(session).edite(
            data=_room_data,
            id=room_id)
        await session.commit()

    return {"status":"ok"}

@router.delete("/{hotel_id}/rooms/{room_id}",summary="Удаление отеля")
async def delete_room(
    hotel_id:int,
    room_id:int,
):
    async with async_session_maker() as session:
        await RoomsRepository(session).delete(
            id=room_id,
            hotel_id=hotel_id)
        await session.commit()
    return {"ststus":"ok"}