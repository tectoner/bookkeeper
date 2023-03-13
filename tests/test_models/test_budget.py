import pytest

from bookkeeper.models.budget import Budget

def test_create_with_full_args_list():
    b = Budget(period='День', limit=100, spent=20, pk=1)
    assert b.period == 'День'
    assert b.limit == 100
    assert b.spent == 20


def test_period_values():
    for period in ["День", "Неделя", "Месяц"]:
        b = Budget(period=period, limit=0, spent=0, pk=1)
    
    with pytest.raises(ValueError):
        b = Budget(period='Квартал', limit=2, spent=4, pk=1)