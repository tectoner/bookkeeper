from bookkeeper.repository.sqlite_repository import SQLiteRepository
from bookkeeper.models.expense import Expense
from bookkeeper.models.category import Category
from bookkeeper.models.budget import Budget

import pytest

from os import remove, path
import random


def test_bind_database():
    filepath = 'D:\\Python\\mipt23-python-project-bookkeeper\\bookkeeper\\repository\\'
    test_db_name = 'tmp_test_database.db'

    if path.isfile(filepath + test_db_name):
        remove(filepath + test_db_name)

    SQLiteRepository.bind_database(test_db_name)

@pytest.fixture
def repo_expense():
    return SQLiteRepository[Expense](Expense, Expense.__name__)

@pytest.fixture
def repo_category():
    return SQLiteRepository[Category](Category, Category.__name__)

@pytest.fixture
def repo_budget():
    return SQLiteRepository[Budget](Budget, Budget.__name__)

def test_expense_crud(repo_expense):
    # test add
    objs = []
    pks = []
    for i in range(10):
        p = Expense(amount=float(random.randint(1, 10)), 
                    category=random.randint(1, 10),
                    comment='abc')
        objs.append(p)
        pks.append(repo_expense.add(p))

    assert all([(obj.pk == pk) for (obj, pk) in zip(objs, pks)])

    # test get
    assert all([repo_expense.get(pk) == obj for (obj, pk) in zip(objs, pks)])
    assert all([repo_expense.get(pk) == obj for (obj, pk) in zip(objs, pks)])

    # test update
    obj2 = Expense(amount=1000, category=101000, comment='asdflasdjf')
    obj2.pk = pks[0]
    repo_expense.update(obj2)
    assert repo_expense.get(pks[0]) == obj2

    # test delete
    pks.extend([345, 34589, 123])
    for pk in pks:
        repo_expense.delete(pk)
    assert all([repo_expense.get(pk) == None for pk in pks]) 

def test_category_crud(repo_expense):
    # test add
    objs = []
    pks = []
    for i in range(10):
        p = Expense(amount=float(random.randint(1, 10)), 
                    category=random.randint(1, 10),
                    comment='abc')
        objs.append(p)
        pks.append(repo_expense.add(p))

    assert all([(obj.pk == pk) for (obj, pk) in zip(objs, pks)])

    # test get
    assert all([repo_expense.get(pk) == obj for (obj, pk) in zip(objs, pks)])
    assert all([repo_expense.get(pk) == obj for (obj, pk) in zip(objs, pks)])

    # test update
    obj2 = Expense(amount=1000, category=101000, comment='asdflasdjf')
    obj2.pk = pks[0]
    repo_expense.update(obj2)
    assert repo_expense.get(pks[0]) == obj2

    # test delete
    pks.extend([345, 34589, 123])
    for pk in pks:
        repo_expense.delete(pk)
    assert all([repo_expense.get(pk) == None for pk in pks]) 

def test_budget_crud(repo_budget):
    # test add
    objs = []
    pks = []
    for period in ["День", "Неделя", "Месяц"]:
        p = Budget(period=period, 
                   limit=float(random.randint(1, 10)), 
                   spent=float(random.randint(1, 10)))
        objs.append(p)
        pks.append(repo_budget.add(p))

    assert all([(obj.pk == pk) for (obj, pk) in zip(objs, pks)])

    # test get
    assert all([repo_budget.get(pk) == obj for (obj, pk) in zip(objs, pks)])
    assert all([repo_budget.get(pk) == obj for (obj, pk) in zip(objs, pks)])

    # test update
    obj2 = Budget(period=period, limit=0, spent=0, pk=1)
    obj2.pk = pks[0]
    repo_budget.update(obj2)
    assert repo_budget.get(pks[0]) == obj2

    # test delete
    pks.extend([345, 34589, 123])
    for pk in pks:
        repo_budget.delete(pk)
    assert all([repo_budget.get(pk) == None for pk in pks]) 

def test_category_crud(repo_category):
    # test add
    objs = []
    pks = []
    for cat in ['a', 'b', 'c', 'd']:
        p = Category(name=cat, 
                     parent=None)
        objs.append(p)
        pks.append(repo_category.add(p))

    assert all([(obj.pk == pk) for (obj, pk) in zip(objs, pks)])

    # test get
    assert all([repo_category.get(pk) == obj for (obj, pk) in zip(objs, pks)])
    assert all([repo_category.get(pk) == obj for (obj, pk) in zip(objs, pks)])

    # test update
    obj2 = Category(name='new category', parent=None, pk=1)
    obj2.pk = pks[0]
    repo_category.update(obj2)
    assert repo_category.get(pks[0]) == obj2

    # test delete
    pks.extend([345, 34589, 123])
    for pk in pks:
        repo_category.delete(pk)
    assert all([repo_category.get(pk) == None for pk in pks]) 

def test_cannot_add_with_pk(repo_expense):
    obj = Expense(amount=1000, category=101000, comment='asdflasdjf')
    obj.pk = 1
    with pytest.raises(ValueError):
        repo_expense.add(obj)

def test_cannot_add_without_pk(repo_expense):
    with pytest.raises(ValueError):
        repo_expense.add(0)

def test_get_all_with_condition(repo_expense):
    objs = []

    for i in range(5):
        p = Expense(amount=random.randint(1, 10), 
                    category=10,
                    comment=str(i))
        repo_expense.add(p)
        objs.append(p)
    assert repo_expense.get_all({'comment': '0', 'category': 10}) == [objs[0]]
    assert repo_expense.get_all({'category': 10}) == objs
