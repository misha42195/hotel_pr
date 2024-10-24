from models.facilities import FacilitiesOrm
from repositories.base import BaseRepository
from schemas.facilities import Facilities


class FacilitiesRepository(BaseRepository):
    model = FacilitiesOrm
    schema = Facilities
