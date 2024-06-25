from datetime import date
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.validators import check_booking_exists
from app.core.db import get_async_session
from app.schemas.booking import BookingCreate, BookingDB, BookingUpdate
from app.crud.booking import booking_crud

router = APIRouter()


@router.post('/', response_model=BookingDB, response_model_exclude_none=True)
async def create_new_booking(
    booking: BookingCreate,
    session: AsyncSession = Depends(get_async_session)
):
    '''Создание нового бронирования'''
    try:
        new_booking = await booking_crud.create_booking(booking, session)
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
    '''
    Получение всех бронирований
    '''
    all_bookings = await booking_crud.get_all(session)
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
    '''
    Обновление бронирования
    '''
    booking = await check_booking_exists(booking_id, session)
    updated_booking = await booking_crud.update(booking, booking_in,
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
    '''
    Удаление бронирования
    '''
    booking = await check_booking_exists(booking_id, session)
    updated_booking = await booking_crud.remove(booking, session)
    return updated_booking


@router.get('/booking-by-date/{booking_date}',
            response_model=list[BookingDB], response_model_exclude_none=True)
async def get_bookings_by_date(
    booking_date: date,
    session: AsyncSession = Depends(get_async_session)
):
    '''
    Возвращает список броней на указанную дату
    '''
    bookings = await booking_crud.get_bookings_by_date(booking_date, session)
    if not bookings:
        raise HTTPException(
            status_code=404, detail="На данную дату бронь не найдена")
    return bookings


@router.get('/free-by-date/{booking_date}',
            response_model=list[int], response_model_exclude_none=True)
async def get_free_hours_by_date(
    booking_date: date,
    session: AsyncSession = Depends(get_async_session)
):
    '''
    Возвращает список свободных часов на указанную дату
    '''
    free_hours = await booking_crud.get_free_by_date_any_workplace(
        booking_date, session
    )
    if not free_hours:
        raise HTTPException(
            status_code=404, detail="На данную дату нет свободных мест")
    return free_hours
