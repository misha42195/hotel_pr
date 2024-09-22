from fastapi import HTTPException
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
        # Проверка на наличие полей модели через __table__.columns
        filters = []
        for key, value in filter_by.items():
            if key not in self.model.__table__.columns:
                raise AttributeError(f"Модель {self.model.__name__} не имеет атрибута '{key}'")
            filters.append(getattr(self.model, key) == value)

        query = select(self.model).where(*filters)
        result = await self.session.execute(query)
        return result.scalars().one_or_none()

    async def add(self, data: BaseModel):
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

    async def edite(self, data: BaseModel, **filter_by) -> None:
        # Проверка на наличие полей модели через __table__.columns
        filters = []
        for key, value in filter_by.items():
            filters.append(getattr(self.model, key) == value)

        # Проверяем, что объект существует
        hotel_object = await self.get_one_or_none(**filter_by)
        if not hotel_object:
            raise HTTPException(status_code=404, detail="Отель не найден")

        # Выполняем обновление
        update_data_stmt = (
            update(self.model)
            .where(*filters)
            .values(**data.model_dump())
            .returning(self.model)
        )
        print(update_data_stmt.compile(engine, compile_kwargs={"literal_binds": True}))
        result = await self.session.execute(update_data_stmt)
        updated_hotel = result.scalars().one_or_none()

        if not updated_hotel:
            raise HTTPException(status_code=404, detail="Невозможно обновить объект")

        return updated_hotel
