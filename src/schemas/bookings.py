from datetime import date

from pydantic import BaseModel, ConfigDict
from pydantic.mypy import from_attributes_callback


# схема запроса получения даты
class BookingRequestAdd(BaseModel):
    room_id: int
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

    model_config = ConfigDict(from_attributes=True)
