from sqlalchemy import select, insert
from src.database import engine
from sqlalchemy.orm import Session
from src.models.hotels import HotelsOrm


class BaseRepository:
    model = None

    def __init__(self, session):
        self.session = session

    async def get_all(self, *args, **kwargs):
        query = select(self.model)
        result = await self.session.execute(query)
        print(query.compile(engine, compile_kwargs={"literal_binds": True}))
        result = result.scalars().all()
        return result

    async def get_one_or_none(self, **filter_by):
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        return result.scalars().one_or_none()

    async def add_hotel(
            self,
            title,
            location
    ):
        add_hotel_stmt = (
            insert(self.model)
            .values(title=title, location=location)
            .returning(self.model)
        )
        print(add_hotel_stmt.compile(engine, compile_kwargs={"literal_binds": True}))
        result = await self.session.execute(add_hotel_stmt)
        hotel = result.scalars().all()
        print(hotel)
        return hotel