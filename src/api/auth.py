from datetime import datetime, timezone, timedelta

import jwt
from fastapi import APIRouter, HTTPException
from fastapi import Response
from passlib.context import CryptContext
from starlette.requests import Request

from src.config import settings
from src.database import async_session_maker
from src.repositories.users import UsersRepository
from src.schemas.users import UserRequestAdd, UserAdd, User
from src.service.auth import AuthService

router = APIRouter(prefix="/auth", tags=["Аутентификация и авторизация"])


@router.post("/login",summary="Авторизация пользователя")
async def login_user(
        data: UserRequestAdd,
        response: Response
):
    async with async_session_maker() as session:
        user = await UsersRepository(session).get_user_with_hashed_password(email=data.email)
        if not user:
            raise HTTPException(status_code=401, detail="Пользователь с такой почтой не зарегистрирован")
        if not AuthService().verify_password(data.password, user.hashed_password):
            raise HTTPException(status_code=401, detail="Неправильный пароль")
        access_token = AuthService().create_access_token({"user_id": user.id})
        response.set_cookie("access_token", access_token)
        return {"access_token": access_token}


@router.post("/register", summary="Регистрация пользователя")
async def register_user(
        data: UserRequestAdd
):  # получаем данные на регистрацию
    hash_password = AuthService().hashed_password(data.password)  # преобразуем значение входящего пароля в хеш-значение
    print("пароль=", hash_password)
    new_user_data = UserAdd(
        nickname=data.nickname,
        email=data.email,
        first_name=data.first_name,
        last_name=data.last_name,
        hashed_password=hash_password  # пароль получим из хеш-функции
    )
    async with async_session_maker() as session:
        user = await UsersRepository(session).add(new_user_data)
        await session.commit()
    return {"status": "ok" , "user": user}


@router.get("/only_auth")
async def only_auth(
        request: Request
):
    # что бы получить значение токена access_token
    # access_token = request # <starlette.requests.Request object at 0x7fb163dac110>
    # access_token = request.cookies # {
    # 'access_token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoyNCwiZXhwIjoxNzI3Nzc3Mzc0fQ.uiMk_SRGtRffKOh8tLk7oAJZWc7en1kXBXpq3O1NoZA'
    # }

    access_token = request.cookies.get("access_token") # eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoyNCwiZXhwIjoxNzI3Nzc3Mzc0fQ.uiMk_SRGtRffKOh8tLk7oAJZWc7en1kXBXpq3O1NoZA

    print(access_token)
