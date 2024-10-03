from fastapi import Query, Depends, Request, HTTPException
from pydantic import BaseModel
from typing import Annotated

from src.service.auth import AuthService


class PaginationParam(BaseModel):
    page: Annotated[int | None, Query(1, ge=1, description="номер страницы")]
    per_page: Annotated[int | None, Query(None, ge=1, lt=30, description="кол-во отелей на странице")]


PaginationDep = Annotated[PaginationParam, Depends()]


def get_token(request: Request) -> str:
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=401, detail="У вас нет токена")
    return token


def get_current_user_id(token: str = Depends(get_token)) -> int:
    data = AuthService().decode_token(token)
    user_id = data.get("user_id", None)
    return user_id


UserIdDep = Annotated[int, Depends(get_current_user_id)]
