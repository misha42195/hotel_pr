from fastapi import APIRouter
from fastapi.params import Query, Body

from api.dependenies import DBDep
from schemas.facilities import Facilities, FacilitiesAdd

router = APIRouter(prefix="/facilities", tags=["получение удобств"])


@router.get("", summary="Получение удобств")
async def get_facilities(
        db: DBDep,
        title: str | None = Query(None, examples={"title": "Интернет"})
):
    return await db.facilities.get_all(title=title)


@router.post("", summary="создание удобств")
async def create_facilitt(
        db: DBDep,
        facility_date: FacilitiesAdd = Body(openapi_examples={
            "1": {
                "value": {
                    "title": "Интернет",
                }
            }
        })
):
    facility = await db.facilities.add(data=facility_date)
    await db.commit()
    return {"ststus": "ok", "facility": facility}
