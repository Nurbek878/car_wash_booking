from datetime import datetime
from pydantic import BaseModel, Field, validator

from app.utils.time_utils import FROM_TIME


class BookingBase(BaseModel):
    booking_from: datetime = Field(..., description='Время'
                                   'начала бронирования', example=FROM_TIME)
    brand: str = Field(..., description='Марка автомобиля')
    model: str = Field(..., description='Модель автомобиля')
    number: str = Field(..., description='Номер автомобиля')


class BookingCreate(BookingBase):

    @validator('booking_from')
    def validate_booking_from(cls, value):
        value = value.replace(tzinfo=None)
        now = datetime.now().replace(tzinfo=None)
        if value <= now:
            raise ValueError('Время бронирования не может быть меньше '
                             'настоящего')
        booking_hour = value.hour
        if booking_hour < 9 or booking_hour >= 18:
            raise ValueError('время бронирования должно быть между '
                             '09:00 и 18:00')
        return value


class BookingDB(BookingBase):
    id: int
    workplace_id: int
    booking_to: datetime = Field(..., description='Время окончания'
                                 'бронирования')

    class Config:
        orm_mode = True
