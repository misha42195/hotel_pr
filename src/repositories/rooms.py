from sqlalchemy import select


from src.models.rooms import RoomsOrm
from src.repositories.base import BaseRepository
from src.schemas.rooms import Room

class RoomsRepository(BaseRepository):
    model = RoomsOrm
    schema = Room

    async def get_all(self,
                title,
                description,
                ):
        query = select(RoomsOrm)
        if title:
            query = query.filter(RoomsOrm.title.ilike(f"%{title}%"))
            print("query_title=",query)
        if description:
            query = query.filter(RoomsOrm.description.ilike(f"%{description}%"))
            print("query_description=",query)
        

        result = await self.session.execute(query)
        result = result.scalars().all()

        return result
