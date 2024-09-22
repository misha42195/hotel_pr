from sqlalchemy import select

from src.repositories.base import BaseRepository
from src.database import engine
from src.models.hotels import HotelsOrm


class HotelsRepository(BaseRepository):
    model = HotelsOrm

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
