from sqlalchemy import Column, ForeignKey, Integer, Text

from app.models.abstract import Abstract


class Donation(Abstract):
    """
    Модель для представления пожертвования в БД.
    """
    user_id = Column(Integer, ForeignKey('user.id'))
    comment = Column(Text)

    def __repr__(self):
        return (
            f'Donation(full_amount={self.full_amount}, '
            f'invested_amount={self.invested_amount})'
        )

    def __str__(self):
        return (
            f'Пожертвование на сумму {self.full_amount}, '
            f'из них инвестировано {self.invested_amount}'
        )