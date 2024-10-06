from pydantic import BaseModel, Field

    

class RoomAdd(BaseModel):

    hotel_id: int
    title: str
    description: str
    price:int
    quantity: int

class Room(RoomAdd):
    id: int



class RoomPatch(BaseModel):
    hotel_id: int| None = Field(default=None, description="Id отеля")
    title: str| None = Field(default=None, description="Название номера")
    description: str| None = Field(default=None, description="Описание номера")
    price:int| None = Field(default=None, description="Стомость номера")
    quantity: int = Field(default=None,description="Кол-во номеров")

class RoomPut(BaseModel):
    hotel_id: int
    title: str
    description: str
    price:int
    quantity: int