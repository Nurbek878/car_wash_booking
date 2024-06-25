from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.booking import get_booking_by_id
from app.crud.workplace import get_workplace_by_id, get_workplace_id_by_name
from app.models import Workplace
from app.models import Booking


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


async def check_booking_exists(
        booking_id: int,
        session: AsyncSession,
) -> Booking:
    booking = await get_booking_by_id(booking_id, session)
    if not booking:
        raise HTTPException(status_code=404,
                            detail="Бронь не найдена")
    return booking
