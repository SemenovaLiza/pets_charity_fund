from typing import List, Optional

from sqlalchemy import select

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.charity_project import CharityProject
from app.schemas.charity_project import CharityProjectCreate


async def create_charity_project(
        new_project: CharityProjectCreate,
        session: AsyncSession
) -> CharityProject:
    new_project_data = new_project.dict()
    db_project = CharityProject(**new_project_data)
    session.add(db_project)
    await session.commit()
    await session.refresh(db_project)
    return db_project


async def get_project_id_by_name(
        project_name: str,
        session: AsyncSession
) -> Optional[int]:
    db_project_id = await session.execute(
        select(CharityProject.id).where(
            CharityProject.name == project_name
        )
    )
    db_project_id = db_project_id.scalars().first()
    return db_project_id


async def read_all_projects_from_db(session: AsyncSession) -> List[CharityProject]:
    db_projects = await session.execute(select(CharityProject))
    return db_projects.scalars().all() 