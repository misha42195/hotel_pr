from sqlalchemy import select, delete, insert

from src.models.facilities import FacilitiesOrm, RoomsFacilitiesOrm
from src.repositories.base import BaseRepository
from src.repositories.mappers.mappers import FacilitiesDataMapper
from src.schemas.facilities import RoomFacility


class FacilitiesRepository(BaseRepository):
    model = FacilitiesOrm
    mapper = FacilitiesDataMapper


class RoomsFacilitiesRepository(BaseRepository):
    model = RoomsFacilitiesOrm
    schema = RoomFacility

    async def set_facilities(self, room_id: int, facilities_ids: list[int]):
        # получим текущий список id удобств
        current_facilities_ids_query = (
            select(self.model.facility_id)
            .filter_by(room_id=room_id)
        )
        res = await self.session.execute(current_facilities_ids_query)
        current_facilities_ids = res.scalars().all()  # список текущих удобств

        # определяемся со списком для удаления
        facilities_ids_to_delete = list(set(current_facilities_ids) - set(facilities_ids))

        # список для добавления
        facilities_ids_to_append = list(set(facilities_ids) - set(current_facilities_ids))

        # если есть значения для удаления, напишем запрос на удаление
        if facilities_ids_to_delete:
            delete_stmt = (
                delete(self.model)
                .filter(
                    self.model.room_id == room_id,
                    self.model.facility_id.in_(facilities_ids_to_delete)
                )
            )
            await self.session.execute(delete_stmt)

        if facilities_ids_to_append:
            insert_stmt = (
                insert(self.model)
                .values([{"room_id": room_id, "facility_id": f_ids} for f_ids in facilities_ids_to_append])
            )
            await self.session.execute(insert_stmt)
