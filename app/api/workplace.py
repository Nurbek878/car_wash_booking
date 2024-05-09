from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session

from app.crud.workplace import create_workplace, get_workplace_id_by_name
from app.schemas.workplace import WorkplaceCreate, WorkplaceDB

router = APIRouter()


@router.post(
    "/workplaces/",
    response_model=WorkplaceDB,
    response_model_exclude_none=True,
)
async def create_new_workplace(
    workplace: WorkplaceCreate,
    session: AsyncSession = Depends(get_async_session),
):
    workplace_id = await get_workplace_id_by_name(workplace.name, session)
    if workplace_id is not None:
        raise HTTPException(
            status_code=422,
            detail=" Моечный пост с таким названием уже существует!",
        )
    new_workplace = await create_workplace(workplace, session)
    return new_workplace
