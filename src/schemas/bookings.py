from datetime import date

from pydantic import BaseModel


# схема запроса получения даты
class BookingResponseDateAdd(BaseModel):
    date_from: date
    date_to: date


# схема добавления бронирования
class BookingAdd(BaseModel):
    user_id: int
    room_id: int
    date_from: date
    date_to: date
    price: int


class Booking(BookingAdd):
    id: int
