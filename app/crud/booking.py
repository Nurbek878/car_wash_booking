from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from app.models.booking import Booking
from app.models.workplace import Workplace
from app.schemas.booking import BookingCreate


async def get_first_available_workplace(booking_from: datetime,
                                        session: AsyncSession) -> int:
    one_hour_later = booking_from + timedelta(hours=1)

    # Подзапрос для получения всех занятых боксов на указанный период
    subquery = select(Booking.workplace_id).where(
        and_(
            Booking.booking_from < one_hour_later,
            booking_from < Booking.booking_from + timedelta(hours=1)
        )
    ).subquery()

    # Основной запрос для получения первого свободного бокса
    result = await session.execute(
        select(Workplace.id).where(Workplace.id.notin_(subquery))
    )
    available_workplace = result.scalars().first()

    if available_workplace is None:
        raise ValueError("Нет доступных боксов на указанное время.")

    return available_workplace


async def is_booking_conflict(session: AsyncSession,
                              new_booking: BookingCreate) -> bool:
    one_hour_later = new_booking.booking_from + timedelta(hours=1)
    conflict_query = select(Booking).where(
        and_(
            Booking.brand == new_booking.brand,
            Booking.model == new_booking.model,
            Booking.number == new_booking.number,
            Booking.booking_from < one_hour_later,
            new_booking.booking_from < Booking.booking_to
        )
    )

    result = await session.execute(conflict_query)
    return result.scalars().first() is not None


async def create_booking(new_booking: BookingCreate,
                         session: AsyncSession) -> Booking:
    if await is_booking_conflict(session, new_booking):
        raise ValueError('Автомобиль данной марки и модели с таким номером '
                         'уже забронирован на это же время.')
    booking_dict = new_booking.dict()
    booking_dict['booking_to'] = booking_dict['booking_from'] + timedelta(
        hours=1)

    # Получаем первый доступный бокс
    booking_dict['workplace_id'] = await get_first_available_workplace(
        booking_dict['booking_from'], session)

    db_booking = Booking(**booking_dict)
    session.add(db_booking)
    await session.commit()
    await session.refresh(db_booking)
    return db_booking


async def read_all_bookings_from_db(
    session: AsyncSession,
) -> list[Booking]:
    db_bookings = await session.execute(select(Booking))
    return db_bookings.scalars().all()
