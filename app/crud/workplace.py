from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.workplace import Workplace


class CRUDWorkplace(CRUDBase):

    async def get_workplace_id_by_name(
        self,
        worklplace_name: str,
        session: AsyncSession,
    ) -> Optional[int]:
        db_workplace_id = await session.execute(
            select(Workplace.id).where(Workplace.name == worklplace_name)
        )
        db_workplace_id = db_workplace_id.scalars().first()
        return db_workplace_id


workplace_crud = CRUDWorkplace(Workplace)
