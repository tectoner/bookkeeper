from pytestqt.qt_compat import qt_api

from PySide6 import QtWidgets, QtCore

from bookkeeper.view.budget_table_view import BudgetWidget

class CallbackChecker():
    def __init__(self):
        self.called = False
        self.args = None
        self.kwargs = None

    def check_callback(self, *args, **kwargs):
        self.called = True
        self.args = args
        self.kwargs = kwargs

def test_create(qtbot):
    user_data = [['1', 'Day', '1000', '500', '200'], ['2', 'Week', '200', '600', '100']]
    f = lambda x, y: x + y

    widget = BudgetWidget()
    qtbot.addWidget(widget)

    widget.set_data(user_data)
    assert widget.user_data == user_data

    widget.register_update_callback(f)
    assert widget.update_callback == f

    tab = widget.table
    assert tab.columnCount() == 4
    assert tab.rowCount() == len(user_data)

def test_editable(qtbot):
    callback_checker = CallbackChecker()
    user_data = [['1', 'Day', '1000', '500', '200'], ['2', 'Week', '200', '600', '100']]

    widget = BudgetWidget()
    qtbot.addWidget(widget)

    widget.set_data(user_data)

    assert widget.table.columnCount() == 4
    assert widget.table.rowCount() == len(user_data)

    for row in range(len(user_data)):
        for col in range(4):
            item = QtWidgets.QTableWidgetItem(widget.table.item(row, col))
            if col == 2:  # limit column
                assert item.flags() == (QtCore.Qt.ItemFlag.ItemIsEditable |
                                        QtCore.Qt.ItemFlag.ItemIsSelectable |
                                        QtCore.Qt.ItemFlag.ItemIsEnabled)
            else:
                assert item.flags() == (QtCore.Qt.ItemFlag.ItemIsSelectable |
                                        QtCore.Qt.ItemFlag.ItemIsEnabled)


def test_update(qtbot):
    callback_checker = CallbackChecker()
    user_data = [['1', 'Day', '1000', '500', '200'], ['2', 'Week', '200', '600', '100']]

    widget = BudgetWidget()
    qtbot.addWidget(widget)

    widget.set_data(user_data)
    widget.register_update_callback(callback_checker.check_callback)

    widget.table.cellClicked.emit(0, 2)
    assert callback_checker.called == False
    widget.table.item(0, 2).setText('4000')
    assert callback_checker.called == True
    assert callback_checker.args[0] == '1' and callback_checker.args[1] == '4000'



