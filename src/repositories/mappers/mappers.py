from src.models.bookings import BookingsOrm
from src.models.facilities import FacilitiesOrm
from src.models.users import UsersOrm
from src.schemas.bookings import Booking
from src.schemas.facilities import Facility
from src.schemas.users import User
from src.models.hotels import HotelsOrm
from src.models.rooms import RoomsOrm
from src.schemas.hotels import Hotel
from src.schemas.rooms import Room, RoomWithReal
from src.repositories.mappers.base import DataMapper


class HotelsDataMapper(DataMapper):
    db_model = HotelsOrm
    schema = Hotel


class RoomsDataMapper(DataMapper):
    db_model = RoomsOrm
    schema = Room


class UsersDataMapper(DataMapper):
    db_model = UsersOrm
    schema = User


class FacilitiesDataMapper(DataMapper):
    db_model = FacilitiesOrm
    schema = Facility


class BookingsDataMapper(DataMapper):
    db_model = BookingsOrm
    schema = Booking


class RoomDataWithRealsMapper(DataMapper):
    db_model = RoomsOrm
    schema = RoomWithReal
