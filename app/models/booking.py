from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from app.core.db import Base


class Booking(Base):
    booking_from = Column(DateTime, nullable=False)
    booking_to = Column(DateTime, nullable=False)
    workplace_id = Column(Integer, ForeignKey('workplace.id'), nullable=False)
    brand = Column(String, nullable=False)
    model = Column(String, nullable=False)
    number = Column(String, nullable=False)
