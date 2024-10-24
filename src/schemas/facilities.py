from pydantic import BaseModel


class FacilitiesAdd(BaseModel):
    title: str


class Facilities(FacilitiesAdd):
    id: int

    class Config:
        from_attributes = True
