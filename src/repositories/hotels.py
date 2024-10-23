from datetime import date

from sqlalchemy import select

from models.rooms import RoomsOrm
from repositories.utils import rooms_id_for_booking
from src.repositories.base import BaseRepository
from src.database import engine
from src.models.hotels import HotelsOrm
from src.schemas.hotels import Hotel
from src.repositories.utils import rooms_id_for_booking


class HotelsRepository(BaseRepository):
    model = HotelsOrm
    schema = Hotel

    async def get_all(self,
                      title,
                      location,
                      limit,
                      offset):

        query = select(HotelsOrm)
        if title:
            query = query.filter(HotelsOrm.title.ilike(f"%{title}%"))
            print(f"query_title=", query)
        if location:
            query = query.filter(HotelsOrm.location.ilike(f"%{location}%"))
            print(f"query_title=", query)
        query = (
            query
            .limit(limit)  # ограничение на кол-во объектов
            .offset(offset)  # кол-во отображенных объектов на пред.стр
        )
        print(query.compile(engine, compile_kwargs={"literal_binds": True}))
        result = await self.session.execute(query)
        result = result.scalars().all()
        return result

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
        )

        if title is not None:
            hotels_ids_to_get = (
                hotels_ids_to_get.filter(HotelsOrm.title.ilike(f"%{title}%"))
                .subquery("hotels_ids_to_get")
            )

        if location is not None:
            hotels_ids_to_get = (
                hotels_ids_to_get.filter(HotelsOrm.location.ilike(f"%{location}%"))
                .subquery("hotels_ids_to_get")
            )

        # запрос на получение id отелей
        hotels_ids_to_get = (
            select(RoomsOrm.hotel_id)
            .select_from(RoomsOrm)
            .limit(limit)
            .offset(offset)
            .filter(RoomsOrm.id.in_(rooms_ids_to_get))
        )
        return await self.get_filtered(HotelsOrm.id.in_(hotels_ids_to_get))
