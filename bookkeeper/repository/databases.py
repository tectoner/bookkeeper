"""
Module with sqlite3 database structure
"""
from typing import Any

import pony.orm as pny  # type: ignore
from bookkeeper.utils import NONE_2_INT_CHANGER  # type: ignore


db = pny.Database()


class DatabaseHelper():
    """ Contains static methods to work with sqlite3 database """
    @staticmethod
    def get_table_by_name(name: str) -> db.Entity:
        """ Get database class entity by table name"""
        if name == 'Expense':
            return Expense
        if name == 'Category':
            return Category
        if name == 'Budget':
            return Budget

        return Expense


class Expense(db.Entity):
    """ ORM for database table Expense"""
    pk = pny.PrimaryKey(int, auto=True)
    amount = pny.Required(float)
    category = pny.Required(int)
    comment = pny.Optional(str, 50)
    added_date = pny.Required(str, 30)
    expense_date = pny.Optional(str, 30)

    def get_data(self) -> dict[str, Any]:
        """ Get data from entity """
        return {
            'pk': self.pk,
            'amount': self.amount,
            'category': self.category,
            'comment': self.comment,
            'added_date': self.added_date,
            'expense_date': self.expense_date
        }


class Category(db.Entity):
    """ ORM for database table Category"""
    pk = pny.PrimaryKey(int, auto=True)
    parent = pny.Optional(int)
    name = pny.Required(str, 30)

    def get_data(self) -> dict[str, Any]:
        """ Get data from entity """
        return {
            'pk': self.pk,
            'parent': None if self.parent == NONE_2_INT_CHANGER else self.parent,
            'name': self.name
        }


class Budget(db.Entity):
    """ ORM for database table Budget"""
    pk = pny.PrimaryKey(int, auto=True)
    period = pny.Required(str, 20)
    limit = pny.Required(float)
    spent = pny.Required(float)

    def get_data(self) -> dict[str, Any]:
        """Get data from entity """
        return {
            'pk': self.pk,
            'period': self.period,
            'limit': self.limit,
            'spent': self.spent
        }
