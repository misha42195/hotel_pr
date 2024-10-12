from sqlalchemy import text
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from src.config import settings
from sqlalchemy.orm import DeclarativeBase

engine = create_async_engine(settings.DB_URL)

async_session_maker = async_sessionmaker(bind=engine, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


from sqlalchemy import MetaData

metadata = MetaData()


async def del_rooms():
    if 'rooms' in metadata:
        print(metadata.tables['rooms'])
        metadata.remove(metadata.tables['rooms'])
        print("Удалено")
    else:
        print("НЕТ данных")
