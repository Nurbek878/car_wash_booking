from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.db import get_async_session
from app.schemas.booking import BookingCreate, BookingDB
from app.crud.booking import create_booking

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
