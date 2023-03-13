from pytestqt.qt_compat import qt_api
import pytest
from PySide6 import QtWidgets, QtCore

from bookkeeper.view.main_window import MainWindow

from bookkeeper.view import budget_table_view, expense_table_view, categories_view

def create_window(qtbot):
    w = MainWindow(None)
    qtbot.addWidget(w)

    w.adjust_window_to_screen()

    w1 = budget_table_view.BudgetWidget()
    w2 = expense_table_view.MainTableWidget()
    w3 = categories_view.MainCategoryWidget()

    w.set_widgets(w1, w2, w3)

    widgets = [w.my_layout.itemAt(i) for i in range(3)]

    assert widgets == [w1, w2, w3]

    w.close()