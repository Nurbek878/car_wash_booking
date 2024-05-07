from fastapi import APIRouter, HTTPException

from app.crud.workplace import create_workplace, get_workplace_id_by_name
from app.schemas.workplace import WorkplaceCreate, WorkplaceDB

router = APIRouter()


@router.post(
    "/workplaces/",
    response_model=WorkplaceDB,
    response_model_exclude_none=True,
)
async def create_new_workplace(
    meeting_room: WorkplaceCreate,
):
    workplace_id = await get_workplace_id_by_name(meeting_room.name)
    if workplace_id is not None:
        raise HTTPException(
            status_code=422,
            detail=" Моечный пост с таким названием уже существует!",
        )
    new_room = await create_workplace(meeting_room)
    return new_room
