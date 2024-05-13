from typing import Optional

from pydantic import BaseModel, Field, validator


class WorkplaceBase(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = None


class WorkplaceCreate(WorkplaceBase):
    name: str = Field(..., min_length=1, max_length=100)


class WorkplaceUpdate(WorkplaceBase):

    @validator('name')
    def name_cannot_be_null(cls, value):
        if value is None:
            raise ValueError('Моечный пост не может быть пустым!')
        return value


class WorkplaceDB(WorkplaceCreate):
    id: int

    class Config:
        orm_mode = True
