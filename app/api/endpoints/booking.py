from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.db import get_async_session
from app.models import Booking
from app.schemas.booking import BookingCreate, BookingDB, BookingUpdate
from app.crud.booking import (create_booking, delete_booking,
                              get_booking_by_id, read_all_bookings_from_db,
                              update_booking)

router = APIRouter()


@router.post('/', response_model=BookingDB, response_model_exclude_none=True)
async def create_new_booking(
    booking: BookingCreate,
    session: AsyncSession = Depends(get_async_session)
):
    try:
        new_booking = await create_booking(booking, session)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return new_booking


@router.get(
    "/",
    response_model=list[BookingDB],
    response_model_exclude_none=True,
)
async def read_all_bookings(session: AsyncSession = Depends(
                              get_async_session)):
    all_bookings = await read_all_bookings_from_db(session)
    return all_bookings


@router.patch(
    "/{booking_id}",
    response_model=BookingDB,
    response_model_exclude_none=True,
)
async def update_booking_by_id(
    booking_id: int,
    booking_in: BookingUpdate,
    session: AsyncSession = Depends(get_async_session),
):
    booking = await check_booking_exists(booking_id, session)
    updated_booking = await update_booking(booking, booking_in,
                                           session)
    return updated_booking


@router.delete(
    "/{booking_id}",
    response_model=BookingDB,
    response_model_exclude_none=True,
)
async def delete_booking_by_id(
    booking_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    booking = await check_booking_exists(booking_id, session)
    updated_booking = await delete_booking(booking, session)
    return updated_booking


async def check_booking_exists(
        booking_id: int,
        session: AsyncSession,
) -> Booking:
    booking = await get_booking_by_id(booking_id, session)
    if not booking:
        raise HTTPException(status_code=404,
                            detail="Бронь не найдена")
    return booking
