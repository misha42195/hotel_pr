from src.schemas.bookings import BookingAdd, BookingRequestAdd
from fastapi import APIRouter
from src.api.dependenies import DBDep, UserIdDep

router = APIRouter(prefix="/bookings", tags=["Бронирование номеров"])


@router.post("")
async def add_booking(
        db: DBDep,
        booking_date: BookingRequestAdd,
        user_id: UserIdDep
):
    room = await db.rooms.get_one_or_none(id=booking_date.room_id)
    room_price: int = room.price
    _booking_data = BookingAdd(
        user_id=user_id,
        price=room_price,
        **booking_date.model_dump()
    )
    booking = await db.bookings.add(_booking_data)
    await db.commit()
    return {"status": "ok", "booking": booking}


@router.get("/bookings")
async def get_all_bookings(db: DBDep):
    bookings = await db.bookings.get_all()
    return {"status": "ok", "bookings": bookings}


@router.get("/bookings/me")
async def get_me_bookings(
        user_id: UserIdDep,
        db: DBDep
):
    bookings = await db.bookings.get_all_my_bookings(user_id=user_id)
    return {"status": "ok", "bookings": bookings}
