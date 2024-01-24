from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (check_charity_project_exists,
                                check_charity_project_is_closed,
                                check_charity_project_is_invested,
                                check_name_duplicate)
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud.charity_project import charity_project_crud
from app.models import Donation
from app.schemas.charity_project import (CharityProjectCreate,
                                         CharityProjectDB,
                                         CharityProjectUpdate)
from app.services.investment import investing_process

router = APIRouter()


@router.post(
    '/',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def create_charity_project(
    charity_project: CharityProjectCreate,
    session: AsyncSession = Depends(get_async_session),
):
    """Только для суперюзеров.
    Создает благотворительный проект.
    """
    await check_name_duplicate(charity_project.name, session)
    await charity_project_crud.get_project_id_by_name(
        charity_project.name, session
    )
    new_project = await charity_project_crud.create(charity_project, session)
    await investing_process(new_project, Donation, session)
    return new_project


@router.get(
    '/',
    response_model=List[CharityProjectDB],
    response_model_exclude_none=True,
)
async def get_all_charity_projects(
    session: AsyncSession = Depends(get_async_session),
):
    """Получает список всех проектов."""
    all_projects = await charity_project_crud.get_multi(session)
    return all_projects


@router.patch(
    '/{project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
)
async def update_charity_project(
    project_id: int,
    obj_in: CharityProjectUpdate,
    session: AsyncSession = Depends(get_async_session),
):
    """Только для суперюзеров.
    Закрытый проект нельзя редактировать.
    """
    project = await check_charity_project_exists(
        project_id, session
    )
    check_charity_project_is_closed(project)
    if obj_in.name:
        await check_name_duplicate(obj_in.name, session)
    charity_project = await charity_project_crud.update(
        project, obj_in, session
    )
    return charity_project


@router.delete(
    '/{project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
)
async def delete_charity_project(
    project_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    """Только для суперюзеров.
    Удаляет проект, если в него еще не были инвестированы средства.
    """
    project = await check_charity_project_exists(
        project_id, session
    )
    check_charity_project_is_invested(project)
    charity_project = await charity_project_crud.remove(
        project, session
    )
    return charity_project