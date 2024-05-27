from datetime import datetime
from pydantic import BaseModel, validator, Field


class BookingBase(BaseModel):
    booking_from: datetime = Field(..., description='Время'
                                   'начала бронирования')

    @validator('booking_from')
    def validate_booking_from(cls, value):
        now = datetime.now()
        if value.minute != 0 or value.second != 0 or value.microsecond != 0:
            raise ValueError('Время начала должно быть ровным часом.')
        if value.hour < 9 or value.hour > 19:
            raise ValueError('Время начала должно быть между 09:00 и 19:00.')
        if value <= now:
            raise ValueError('Время начала бронирования не может быть'
                             'меньше текущего времени.')
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
