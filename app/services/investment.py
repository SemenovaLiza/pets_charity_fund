from datetime import datetime
from typing import List, Union

from app.models import CharityProject, Donation


async def close_donation_for_obj(obj_in: Union[CharityProject, Donation]):
    """
    Закрывает проект, когда внесенные пожертвования
    покрывают требуемую сумму.
    """
    obj_in.invested_amount = obj_in.full_amount
    obj_in.fully_invested = True
    obj_in.close_date = datetime.now()
    return obj_in


async def money_distribution(
    obj_in: Union[CharityProject, Donation],
    obj_model: Union[CharityProject, Donation],
) -> Union[CharityProject, Donation]:
    """
    Функция отвечает за распределение новых пожертвований
    между проектами, не собравшими требуемую для закрытия сумму.
    """
    free_amount_in = obj_in.full_amount - obj_in.invested_amount
    free_amount_in_model = obj_model.full_amount - obj_model.invested_amount

    if free_amount_in > free_amount_in_model:
        obj_in.invested_amount += free_amount_in_model
        await close_donation_for_obj(obj_model)

    elif free_amount_in == free_amount_in_model:
        await close_donation_for_obj(obj_in)
        await close_donation_for_obj(obj_model)

    else:
        obj_model.invested_amount += free_amount_in
        await close_donation_for_obj(obj_in)

    return obj_in, obj_model


def investing_process(
    target: CharityProject,
    sources: List[CharityProject]
) -> List[CharityProject]:
    modified = []
    for source in sources:
        to_invest = target.full_amount - target.invested_amount
        for obj in (target, source):
            obj.invested_amount += to_invest
            if obj.full_amount == obj.invested_amount:
                obj.close_date = datetime.now()
                obj.fully_invested = True
        modified.append(source)
        if target.fully_invested:
            break
    return modified
