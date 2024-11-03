from fastapi import HTTPException
from sqlalchemy import select, insert, update, delete
from src.database import engine
from pydantic import BaseModel

from src.schemas.users import User


class BaseRepository:
    model = None
    schema: BaseModel = None

    def __init__(self, session):
        self.session = session

    async def get_filtered(self, *filter, **filter_by):
        query = (
            select(self.model)
            .filter(*filter)
            .filter_by(**filter_by)
        )

        result = await self.session.execute(query)
        return [self.schema.model_validate(model) for model in result.scalars().all()]

    async def get_all(self, *args, **kwargs):
        query = select(self.model)
        result = await self.session.execute(query)
        print(query.compile(engine, compile_kwargs={"literal_binds": True}))

        return [self.schema.model_validate(hotel, from_attributes=True) for hotel in result.scalars().all()]

    async def get_one_or_none(self, **filter_by):
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        obj = result.scalars().one_or_none()
        if obj is None:
            return None
        return self.schema.model_validate(obj, from_attributes=True)

    async def add(self, data: BaseModel):
        add_data_stmt = (
            insert(self.model)
            .values(**data.model_dump())
            .returning(self.model)
        )
        print(add_data_stmt.compile(engine, compile_kwargs={"literal_binds": True}))
        result = await self.session.execute(add_data_stmt)
        model = result.scalars().one()
        print("model= ", model)
        return self.schema.model_validate(model, from_attributes=True)

    async def add_bulk(self, data: list[BaseModel]):
        add_data_stmt = (
            insert(self.model)
            .values([item.model_dump() for item in data])
        )
        print(add_data_stmt.compile(engine, compile_kwargs={"literal_binds": True}))
        await self.session.execute(add_data_stmt)

    async def edite(self, data: BaseModel, **filter_by) -> None:
        update_data_stmt = (
            update(self.model)
            .filter_by(**filter_by)
            .values(**data.model_dump(exclude_unset=True))
        )

        print(update_data_stmt.compile(engine, compile_kwargs={"literal_binds": True}))
        await self.session.execute(update_data_stmt)

    async def delete(self, **filter_by):
        delete_data_stmt = delete(self.model).filter_by(**filter_by)
        await self.session.execute(delete_data_stmt)
