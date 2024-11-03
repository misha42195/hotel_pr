from models.facilities import FacilitiesOrm, RoomsFacilitiesOrm
from repositories.base import BaseRepository
from schemas.facilities import Facilities, RoomFacility


class FacilitiesRepository(BaseRepository):
    model = FacilitiesOrm
    schema = Facilities


class RoomsFacilitiesRepository(BaseRepository):
    model = RoomsFacilitiesOrm
    schema = RoomFacility
