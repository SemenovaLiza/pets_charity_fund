from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import CharityProject


async def get_not_fully_invested_objects(
    obj_in: CharityProject,
    session: AsyncSession
) -> List[CharityProject]:
    """
    Возвращает список проектов, которые еще
    не собрали нужную сумму пожертвований.
    """
    objects = await session.execute(
        select(obj_in).where(obj_in.fully_invested == 0
                             ).order_by(obj_in.create_date)
    )
    return objects.scalars().all()