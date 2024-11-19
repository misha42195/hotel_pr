from src.repositories.mappers.mappers import UsersDataMapper
from src.models.users import UsersOrm
from src.repositories.base import BaseRepository
from src.schemas.users import UserWithHashedPassword
from sqlalchemy import select


class UsersRepository(BaseRepository):
    model = UsersOrm
    mapper = UsersDataMapper

    async def get_user_with_hashed_password(self, email):
        query = select(self.model).filter_by(email=email)
        result = await self.session.execute(query)
        result = result.scalars().first()
        if result is None:
            return None
        return UserWithHashedPassword.model_validate(result)
