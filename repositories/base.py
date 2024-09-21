from sqlalchemy import select, insert
from src.database import engine
from pydantic import BaseModel
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

    async def add(self,data: BaseModel):
        add_data_stmt = (
            insert(self.model)
            .values(**data.model_dump())
            .returning(self.model)
        )
        print(add_data_stmt.compile(engine, compile_kwargs={"literal_binds": True}))
        result = await self.session.execute(add_data_stmt)
        hotel = result.scalars().one()
        print(hotel)
        return hotel
