from fastapi import Query, Depends
from pydantic import BaseModel
from typing import Annotated


class PaginationParam(BaseModel):
    page: Annotated[int | None, Query(1, ge=1, description="номер страницы")]
    per_page: Annotated[int | None, Query(None, ge=1, lt=30, description="кол-во отелей на странице")]


PaginationDep = Annotated[PaginationParam, Depends()]