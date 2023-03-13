""" GUI based on PyQt Library"""
from typing import Callable

from bookkeeper.view.expense_table_view import MainTableWidget
from bookkeeper.view.categories_view import MainCategoryWidget
from bookkeeper.view.main_window import MainWindow
from bookkeeper.view.budget_table_view import BudgetWidget


class PyQtView():
    """ GUI for application based on PyQt6 library"""

    def __init__(self) -> None:
        self.window = MainWindow()

        self.expense_view = MainTableWidget()
        self.category_view = MainCategoryWidget()
        self.budget_view = BudgetWidget()

        self.window.set_widgets(self.expense_view, self.category_view, self.budget_view)

    def set_budget_data(self, user_data: list[list[str]]) -> None:
        """Set user data to be displayed. The first element in each row is considered
        as a primary and is not displayed. Primary key is used in callbacks."""
        self.budget_view.set_data(user_data)

    def register_budget_update_callback(self, callback: Callable[[str, str], None]) -> None:
        """ Register budget update callback"""
        self.budget_view.register_update_callback(callback)

    def set_expense_data(self, user_data: list[list[str]]) -> None:
        """Set user data to be displayed. The first element in each row is considered
        as a primary and is not displayed. Primary key is used in callbacks."""
        self.expense_view.set_data(user_data)

    def set_category_data(self, data: list[list[str]]) -> None:
        """ Data format: [['pk1', 'cat1'], ['pk2', 'cat2']]. The first element
        is considered as a primary key and used in callbacks"""
        self.category_view.set_data(data)
        self.expense_view.set_categories([row[1] for row in data])

    def register_category_add_callback(self, callback: Callable[[str], None]) -> None:
        """ Register category add callback"""
        self.category_view.register_add_callback(callback)

    def register_category_del_callback(self, callback: Callable[[str], None]) -> None:
        """ Register category delete callback"""
        self.category_view.register_del_callback(callback)

    def register_expense_add_callback(self, callback: Callable[[dict[str, str]], None]) -> None:
        """ Register expense add callback"""
        self.expense_view.register_add_callback(callback)

    def register_expense_del_callback(self, callback: Callable[[list[str]], None]) -> None:
        """ Register expense delete callback"""
        self.expense_view.register_remove_callback(callback)

    def register_expense_update_callback(self, callback: Callable[[str, dict[str, str]], None]) -> None:
        """ Register expense update callback"""
        self.expense_view.register_update_callback(callback)

    def show_main_window(self) -> None:
        """ Show main window"""
        self.window.show()
