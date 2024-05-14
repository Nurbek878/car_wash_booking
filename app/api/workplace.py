from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.crud.workplace import (
    create_workplace,
    delete_workplace,
    get_workplace_by_id,
    get_workplace_id_by_name,
    read_all_workplaces_from_db, update_workplace
)
from app.models.workplace import Workplace
from app.schemas.workplace import (WorkplaceCreate, WorkplaceDB,
                                   WorkplaceUpdate)


router = APIRouter(
    prefix="/api/workplaces",
    tags=["Workplaces"],
)


@router.post(
    "/",
    response_model=WorkplaceDB,
    response_model_exclude_none=True,
)
async def create_new_workplace(
    workplace: WorkplaceCreate,
    session: AsyncSession = Depends(get_async_session),
):
    await check_name_duplicate(workplace.name, session)
    new_workplace = await create_workplace(workplace, session)
    return new_workplace


@router.get(
    "/",
    response_model=list[WorkplaceDB],
    response_model_exclude_none=True,
)
async def read_all_workplaces(session: AsyncSession = Depends(
                              get_async_session)):
    all_workplaces = await read_all_workplaces_from_db(session)
    return all_workplaces


@router.patch(
    "/{workplace_id}",
    response_model=WorkplaceDB,
    response_model_exclude_none=True,
)
async def update_workplace_by_id(
    workplace_id: int,
    workplace_in: WorkplaceUpdate,
    session: AsyncSession = Depends(get_async_session),
):
    workplace = await check_workplace_exists(workplace_id, session)
    if workplace_in.name is not None:
        await check_name_duplicate(workplace_in.name, session)
    updated_workplace = await update_workplace(workplace, workplace_in,
                                               session)
    return updated_workplace


@router.delete("/{workplace_id}",
               response_model=WorkplaceDB,
               response_model_exclude_none=True)
async def delete_workplace_by_id(
    workplace_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    workplace = await check_workplace_exists(workplace_id, session)
    deleted_workplace = await delete_workplace(workplace, session)
    return deleted_workplace


async def check_workplace_exists(
        workplace_id: int,
        session: AsyncSession,
) -> Workplace:
    workplace = await get_workplace_by_id(workplace_id, session)
    if not workplace:
        raise HTTPException(status_code=404,
                            detail="Моечный пост не найден")
    return workplace


async def check_name_duplicate(
        workplace_name: str,
        session: AsyncSession,
) -> None:
    workplace_id = await get_workplace_id_by_name(workplace_name, session)
    if workplace_id is not None:
        raise HTTPException(
            status_code=422,
            detail='Моечный пост с таким названием уже существует!',
        )
