from fastapi import APIRouter
from passlib.context import CryptContext

from src.database import async_session_maker
from src.repositories.users import UsersRepository
from src.schemas.users import UserRequestAdd, UserAdd, User

router = APIRouter(prefix="/auth", tags=["Аутентификация и авторизация"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.post("/register", summary="Регистрация пользователя")
async def register(data: UserRequestAdd):

    hash_password = pwd_context.hash(data.password)  # преобразуем значение входящего пароля в хеш-значение
    print("пароль=", hash_password)

    async with async_session_maker() as session:
        old_user_data = await UsersRepository(session).get_one_or_none(email=data.email)
        if old_user_data:
            return {"status":"пользователь с такой почтой существует, пожалуйста войдите"}
        else:
            new_user_data = UserAdd(
                nickname=data.nickname,
                email=data.email,
                first_name=data.first_name,
                last_name=data.last_name,
                hashed_password=hash_password
            )

        await UsersRepository(session).add(data=new_user_data)
        await session.commit()
        return {"status":"ok"}
