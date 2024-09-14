from pydantic import BaseModel, Field


class HotelPatch(BaseModel):
    title: str | None = Field(default=None)
    name: str | None = Field(default=None)


class HotelPUT(BaseModel):
    title: str
    name: str