from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.workplace import Workplace
from app.schemas.workplace import WorkplaceCreate, WorkplaceUpdate
from fastapi.encoders import jsonable_encoder


async def create_workplace(
    new_workplace: WorkplaceCreate,
    session: AsyncSession,
) -> Workplace:
    new_workplace = new_workplace.dict()
    db_workplace = Workplace(**new_workplace)
    session.add(db_workplace)
    await session.commit()
    await session.refresh(db_workplace)
    return db_workplace


async def get_workplace_id_by_name(
    worklplace_name: str,
    session: AsyncSession,
) -> Optional[int]:
    db_workplace_id = await session.execute(
        select(Workplace.id).where(Workplace.name == worklplace_name)
    )
    db_workplace_id = db_workplace_id.scalars().first()
    return db_workplace_id


async def read_all_workplaces_from_db(
    session: AsyncSession,
) -> list[Workplace]:
    db_workplaces = await session.execute(select(Workplace))
    return db_workplaces.scalars().all()


async def get_workplace_by_id(
        workplace_id: int,
        session: AsyncSession,
) -> Optional[Workplace]:
    db_workplace = await session.execute(
        select(Workplace).where(
            Workplace.id == workplace_id
        )
    )
    db_workplace = db_workplace.scalars().first()
    return db_workplace


async def update_workplace(
        db_workplace: Workplace,
        workplace_in: WorkplaceUpdate,
        session: AsyncSession,
) -> Workplace:
    obj_data = jsonable_encoder(db_workplace)
    update_data = workplace_in.dict(exclude_unset=True)
    for field in obj_data:
        if field in update_data:
            setattr(db_workplace, field, update_data[field])
    session.add(db_workplace)
    await session.commit()
    await session.refresh(db_workplace)
    return db_workplace
