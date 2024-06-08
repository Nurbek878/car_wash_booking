from datetime import datetime
from pydantic import BaseModel, Field

from app.utils.time_utils import FROM_TIME


class BookingBase(BaseModel):
    booking_from: datetime = Field(..., description='Время'
                                   'начала бронирования', example=FROM_TIME)

    @classmethod
    def validate_booking_from(cls, value):
        value = value.replace(tzinfo=None)
        now = datetime.now().replace(tzinfo=None)
        if value <= now:
            raise ValueError('время бронирования не может быть меньше'
                             'настоящего')
        booking_hour = value.hour
        if booking_hour < 9 or booking_hour >= 18:
            raise ValueError('время бронирования должно быть между'
                             '09:00 и 18:00')

        return value


class BookingCreate(BookingBase):
    pass


class BookingDB(BookingBase):
    id: int
    workplace_id: int
    booking_to: datetime = Field(..., description='Время окончания'
                                 'бронирования')

    class Config:
        orm_mode = True
