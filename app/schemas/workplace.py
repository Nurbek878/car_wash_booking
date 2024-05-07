from typing import Optional

from pydantic import BaseModel, Field


class WorkplaceBase(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str]


class WorkplaceCreate(WorkplaceBase):
    name: str = Field(..., min_length=1, max_length=100)


class WorkplaceDB(WorkplaceCreate):
    id: int

    class Config:
        orm_mode = True
