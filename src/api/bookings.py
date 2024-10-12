from src.schemas.bookings import BookingAdd, BookingResponseDateAdd
from fastapi import APIRouter
from src.api.dependenies import DBDep, UserIdDep

router = APIRouter(prefix="/bookings", tags=["Бронирование номеров"])


@router.post("")
async def create_booking(
        room_id: int,
        db: DBDep,
        booking_date: BookingResponseDateAdd,
        user_id: UserIdDep
):
    room = await db.rooms.get_one_or_none(id=room_id)
    _price = room.model_dump()
    price = _price["price"]
    print(f"Цена={price}")
    _booking_data = BookingAdd(
        user_id=user_id,
        room_id=room_id,
        price=price,
        **booking_date.model_dump()
    )
    print(_booking_data)
    await db.bookings.add(_booking_data)
    await db.commit()
