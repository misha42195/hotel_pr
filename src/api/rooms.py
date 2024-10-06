from fastapi import APIRouter,Query
from src.database import async_session_maker
from src.repositories.rooms import RoomsRepository
from src.schemas.rooms import RoomAdd, RoomPut, RoomPatch

# роутор для номеров
router = APIRouter(prefix="/hotels",tags=["Номера"])

@router.get("/{hotel_id}/rooms",summary="Получение всх номеров")
async def get_hotels(
    # hotel_id: int,
    title:str|None = Query(default=None,description="Название номера"),
    description: str = Query(default=None,description="писание номера")):

    async with async_session_maker() as session:
        rooms = await RoomsRepository(session).get_all(
            title=title,
            description=description)
    return {"status":"ok","rooms":rooms}


@router.get("/{hotel_id}/rooms/{roomm_id}",summary="")
async def get_hotel(
    # hotel_id:int,
    room_id: int,
    ):
    async with async_session_maker() as session:
        room = await RoomsRepository(session).get_one_or_none(id=room_id)
        if not room:
            return {"status": "Отель с указанным индексом не существует"}
        else:
           return {"status":"ok","room":room}
        
@router.post("/{hotel_id}/rooms{rooms_id}",summary="Создание номера")
async def create_room(
    # hotel_id: int,
    room_data: RoomAdd
):
    async with async_session_maker() as session:
        await RoomsRepository(session).add(room_data)
        await session.commit()

    return {"status":"ok"}


@router.put("/{hotel_id}/rooms/{room_id}",summary="Полное изменение номера")
async def full_update_room(
    # hotel_id: int
    room_id: int,
    room_data: RoomPut
):
    async with async_session_maker() as session:
        await RoomsRepository(session).edite(
            data=room_data,
            id=room_id
            )
        await session.commit()

    return {"status":"ok"}


@router.patch("/{hotel_id}/rooms/{room_id}",summary="Частичное изменение номера")
async def upgrade_room(
    # hotel_id: int,
    room_id: int,
    room_data: RoomPatch
):
    async with async_session_maker() as session:
        await RoomsRepository(session).edite(
            data=room_data,
            id=room_id,
            )
        await session.commit()

    return {"status":"ok"}


@router.delete("/{hotel_id}/rooms/{room_id}",summary="Удаление номера")
async def delete_room(
    # hotel_id:int
    room_id:int):
    async with async_session_maker() as session:
        await RoomsRepository(session).delete(id=room_id)
        await session.commit()

        return {"status":"ok"}

