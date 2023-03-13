"""
Budget class
"""

from dataclasses import dataclass


@dataclass(slots=True)
class Budget:
    """
    Budget.
    period -- period for budget
    budget -- money limit
    """
    period: str
    limit: float = 0
    spent: float = 0
    pk: int = 0

    def __init__(self, period: str, limit: float = 0,
                 spent: float = 0, pk: int = 0):

        if period not in ["День", "Неделя", "Месяц"]:
            raise ValueError(f'unsupported value of period <{period}>')
        self.period = period
        self.limit = limit
        self.spent = spent
        self.pk = pk
