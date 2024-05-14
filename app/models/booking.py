from sqlalchemy import Column, DateTime, ForeignKey, Integer

from app.core.db import Base


class Booking(Base):
    booking_from = Column(DateTime)
    workplace_id = Column(Integer, ForeignKey('workplace.id'))
