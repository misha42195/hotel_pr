from sqlalchemy import select, func

from src.repositories.mappers.mappers import HotelsDataMapper
from src.models.rooms import RoomsOrm
from src.repositories.base import BaseRepository
from src.models.hotels import HotelsOrm

from src.repositories.utils import rooms_id_for_booking


class HotelsRepository(BaseRepository):
    model = HotelsOrm
    mapper = HotelsDataMapper

    # async def get_all(self,
    #                   title,
    #                   location,
    #                   limit,
    #                   offset):
    #
    #     query = select(HotelsOrm)
    #     if title:
    #         query = query.filter(HotelsOrm.title.ilike(f"%{title}%"))
    #         print(f"query_title=", query)
    #     if location:
    #         query = query.filter(HotelsOrm.location.ilike(f"%{location}%"))
    #         print(f"query_title=", query)
    #     query = (
    #         query
    #         .limit(limit)  # ограничение на кол-во объектов
    #         .offset(offset)  # кол-во отображенных объектов на пред.стр
    #     )
    #     print(query.compile(engine, compile_kwargs={"literal_binds": True}))
    #     result = await self.session.execute(query)
    #     result = result.scalars().all()
    #     return result

    async def get_filtered_by_time(
            self, title, location, limit, offset, date_from, date_to):

        # запрос на получение id номеров
        rooms_ids_to_get = rooms_id_for_booking(
            date_from=date_from,
            date_to=date_to
        )

        hotels_ids_to_get = (
            select(RoomsOrm.hotel_id)
            .select_from(RoomsOrm)
            .filter(RoomsOrm.id.in_(rooms_ids_to_get))
        )

        query = select(HotelsOrm).filter(HotelsOrm.id.in_(hotels_ids_to_get))
        if title:
            query = query.filter(func.lower(HotelsOrm.title).contains(title.strip().lower()))
        if location:
            query = query.filter(func.lower(HotelsOrm.location).contains(location.strip().lower()))
        query = (
            query.limit(limit)
            .offset(offset)
        )
        result = await self.session.execute(query)
        return [self.mapper.mapper_to_domain_entity(hotel) for hotel in result.scalars().all()]
