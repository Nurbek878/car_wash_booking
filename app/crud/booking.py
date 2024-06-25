from datetime import date, datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, func
from app.crud.base import CRUDBase
from app.models import Booking, Workplace
from app.schemas.booking import BookingCreate


class CRUDBooking(CRUDBase):

    @staticmethod
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

    @staticmethod
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

    async def create_booking(self, new_booking: BookingCreate,
                             session: AsyncSession) -> Booking:
        if await CRUDBooking.is_booking_conflict(session, new_booking):
            raise ValueError('Автомобиль данной марки и модели'
                             'с таким номером '
                             'уже забронирован на это же время.')
        booking_dict = new_booking.dict()
        booking_dict['booking_to'] = booking_dict['booking_from'] + timedelta(
            hours=1)

        # Получаем первый доступный бокс
        booking_dict['workplace_id'
                     ] = await CRUDBooking.get_first_available_workplace(
            booking_dict['booking_from'], session)

        db_booking = Booking(**booking_dict)
        session.add(db_booking)
        await session.commit()
        await session.refresh(db_booking)
        return db_booking

    async def get_future_booking_for_workplace(
            self,
            workplace_id: int,
            session: AsyncSession,
    ):
        bookings = await session.execute(
            select(Booking).where(
                Booking.workplace_id == workplace_id,
                Booking.booking_from > datetime.now()
            )
        )
        bookings = bookings.scalars().all()
        return bookings

    async def get_bookings_by_date(self, booking_date: date,
                                   session: AsyncSession):
        booking_from_date = func.date(Booking.booking_from)
        result = await session.execute(
            select(Booking).where(booking_from_date == booking_date)
        )
        return result.scalars().all()


booking_crud = CRUDBooking(Booking)
