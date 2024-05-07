from typing import Optional
from sqlalchemy import select
from app.core.db import AsyncSessionLocal
from app.models.workplace import Workplace
from app.schemas.workplace import WorkplaceCreate


async def create_workplace(new_workplace: WorkplaceCreate) -> Workplace:
    new_workplace = new_workplace.dict()
    db_workplace = Workplace(**new_workplace)

    async with AsyncSessionLocal() as session:
        session.add(db_workplace)
        await session.commit()
        await session.refresh(db_workplace)
    return db_workplace


async def get_workplace_id_by_name(worlplace_name: str) -> Optional[int]:
    async with AsyncSessionLocal() as session:
        db_workplace_id = await session.execute(
            select(Workplace.id).where(Workplace.name == worlplace_name)
        )
        db_workplace_id = db_workplace_id.scalars().first()
    return db_workplace_id
