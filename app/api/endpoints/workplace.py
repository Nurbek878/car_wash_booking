from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import check_name_duplicate, check_workplace_exists
from app.core.db import get_async_session
from app.crud.booking import get_future_booking_for_workplace
from app.crud.workplace import (
    create_workplace,
    delete_workplace,
    read_all_workplaces_from_db, update_workplace
)
from app.schemas.booking import BookingDB
from app.schemas.workplace import (WorkplaceCreate, WorkplaceDB,
                                   WorkplaceUpdate)


router = APIRouter()


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


@router.get(
    '/{workplace_id}/bookings',
    response_model=list[BookingDB],
)
async def get_bookings_for_workplace(
        workplace_id: int,
        session: AsyncSession = Depends(get_async_session),
):
    await check_workplace_exists(workplace_id, session)
    bookings = await get_future_booking_for_workplace(
        workplace_id=workplace_id, session=session
    )
    return bookings
