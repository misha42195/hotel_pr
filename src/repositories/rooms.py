from datetime import date

from sqlalchemy import select
from sqlalchemy.orm import selectinload

from src.repositories.mappers.mappers import RoomsDataMapper, RoomDataWithRealsMapper
from src.repositories.utils import rooms_id_for_booking
from src.schemas.rooms import RoomWithReal
from src.models.rooms import RoomsOrm
from src.repositories.base import BaseRepository
from src.schemas.rooms import Room


class RoomsRepository(BaseRepository):
    model = RoomsOrm
    mapper = RoomsDataMapper

    async def get_all(self,
                      title,
                      description,
                      ):
        query = select(RoomsOrm)
        if title:
            query = query.filter(RoomsOrm.title.ilike(f"%{title}%"))
            print("query_title=", query)
        if description:
            query = query.filter(RoomsOrm.description.ilike(f"%{description}%"))
            print("query_description=", query)

        result = await self.session.execute(query)
        result = result.scalars().all()

        return result

    async def get_filtered_by_time(
            self,
            hotel_id,
            date_from: date,
            date_to: date):

        rooms_ids_to_get = rooms_id_for_booking(date_from, date_to, hotel_id)
        # print(rooms_ids_to_get.compile(bind=engine, compile_kwargs={"literal_binds": True}))
        # return await self.get_filtered(RoomsOrm.id.in_(rooms_ids_to_get))
        query = (
            select(self.model)
            .options(selectinload(self.model.facilities))
            .filter(RoomsOrm.id.in_(rooms_ids_to_get))
        )
        result = await self.session.execute(query)
        return [RoomWithReal.model_validate(model) for model in result.unique().scalars().all()]

    async def get_one_or_none_with_rels(self, **filter_by):
        query = (
            select(self.model)
            .options(selectinload(self.model.facilities))
            .filter_by(**filter_by)
        )

        result = await self.session.execute(query)
        obj = result.scalars().one_or_none()
        if obj is None:
            return None
        return RoomDataWithRealsMapper.mapper(obj)
