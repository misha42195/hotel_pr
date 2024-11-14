from pydantic import BaseModel


class FacilitiesAdd(BaseModel):
    title: str


class Facility(FacilitiesAdd):
    id: int

    class Config:
        from_attributes = True


class RoomFacilityAdd(BaseModel):
    room_id: int
    facility_id: int


class RoomFacility(RoomFacilityAdd):
    id: int
