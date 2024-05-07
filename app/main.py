from fastapi import FastAPI

from app.core.config import settings
from app.api.workplace import router


app = FastAPI(title=settings.app_title)
app.include_router(router)
