from fastapi import APIRouter

from app.api.endpoints import (workplace_router, booking_router,
                               user_router)

main_router = APIRouter()
main_router.include_router(
    workplace_router, prefix='/workplaces', tags=['Workplaces']
)
main_router.include_router(
    booking_router, prefix='/bookings', tags=['Bookings']
)
main_router.include_router(user_router)
