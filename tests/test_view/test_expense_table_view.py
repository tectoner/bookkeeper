from pytestqt.qt_compat import qt_api
import pytest
from PySide6 import QtWidgets, QtCore

from bookkeeper.view.expense_table_view import InputExpenseWindow, MainTableWidget

class CallbackChecker():
    def __init__(self):
        self.called = False
        self.args = None
        self.kwargs = None

    def check_callback(self, *args, **kwargs):
        self.called = True
        self.args = args
        self.kwargs = kwargs

ctg_options = ['cat1', 'cat2']
msg_dict = {'window_title': 'title', 'save_button_text': 'btn_text'}
def_values = {
    'expense_date': '01-01-2022',
    'amount': '1500.00',
    'category': 'cat1',
    'comment': 'abc'
}
user_data = [
    ['1', '01-01-2022', '1500.0', 'cat1', 'abcde'],
    ['2', '02-01-2022', '1700.0', 'cat2', 'asdfasdf']
]


def test_create_iew(qtbot):

    f = lambda x, y: x + y
    w = InputExpenseWindow(
        parent=None,
        on_clicked_save_callback=f,
        ctg_options=ctg_options,
        msg_dict=msg_dict,
        default_values=def_values
    )
    qtbot.addWidget(w)

    assert w.on_clicked_save_callback == f
    assert w.ctg_options == ctg_options
    assert w.msg_dict == msg_dict

    # check default values
    assert w.get_data() == def_values

    w.close()

    with pytest.raises(KeyError):
        w = InputExpenseWindow(
            parent=None,
            on_clicked_save_callback=f,
            ctg_options=ctg_options,
            msg_dict={'abc': 'cde'},
            default_values=def_values
        )

def test_callback_iew(qtbot):
    callback = CallbackChecker()

    w = InputExpenseWindow(
        parent=None,
        on_clicked_save_callback=callback.check_callback,
        ctg_options=ctg_options,
        msg_dict=msg_dict,
        default_values=def_values
    )
    qtbot.addWidget(w)

    assert callback.called == False
    qtbot.mouseClick(
        w.save_btn,
        qt_api.QtCore.Qt.MouseButton.LeftButton
    )
    w.close()
    assert callback.called == True
    assert callback.args[0] == def_values

def test_create_mtb(qtbot):

    f1 = lambda x: x
    f2 = lambda y: y + y
    f3 = lambda z: z**2
    w = MainTableWidget(None)
    qtbot.addWidget(w)

    w.set_categories(ctg_options)
    w.set_data(user_data)
    w.set_up_table()
    w.register_add_callback(f1)
    w.register_remove_callback(f2)
    w.register_update_callback(f3)

    assert w.cat_data == ctg_options
    assert w.user_data == user_data
    assert w.add_callback == f1
    assert w.remove_callback == f2
    assert w.update_callback == f3

    w.close()

def test_table_mtg(qtbot):

    w = MainTableWidget(None)
    qtbot.addWidget(w)

    w.set_data(user_data)

    assert w.table.columnCount() == 4
    assert w.table.rowCount() == len(user_data)

    for row in range(len(user_data)):
        for col in range(4):
            item = QtWidgets.QTableWidgetItem(w.table.item(row, col))

            assert item.text() == user_data[row][col+1]

            assert item.flags() == (QtCore.Qt.ItemFlag.ItemIsSelectable |
                                        QtCore.Qt.ItemFlag.ItemIsEnabled)

    w.close()

def test_add_callback_mtg(qtbot):
    w = MainTableWidget(None)
    qtbot.addWidget(w)
    w.set_data(user_data)
    w.set_categories(ctg_options)

    callback = CallbackChecker()
    w.register_add_callback(callback.check_callback)

    qtbot.mouseClick(
        w.add_btn,
        qt_api.QtCore.Qt.MouseButton.LeftButton
    )
    assert isinstance(w.input_win, InputExpenseWindow)
    w.input_win.fill_in_default_data(def_values)

    assert callback.called == False

    qtbot.mouseClick(
        w.input_win.save_btn,
        qt_api.QtCore.Qt.MouseButton.LeftButton
    )
    assert callback.called == True
    assert callback.args[0] == def_values

    w.close()

def test_update_callback_mtg(qtbot, monkeypatch):
    w = MainTableWidget(None)
    qtbot.addWidget(w)
    w.set_data(user_data)
    w.set_categories(ctg_options)

    callback = CallbackChecker()
    w.register_update_callback(callback.check_callback)

    # test no rows selected
    monkeypatch.setattr(QtWidgets.QMessageBox, 'exec', lambda *args, **kwargs: QtWidgets.QMessageBox.Ok)
    qtbot.mouseClick(
        w.upd_btn,
        qt_api.QtCore.Qt.MouseButton.LeftButton
    )
    assert w.input_win is None
    assert callback.called == False

    # test many rows selected
    w.table.selectAll()
    monkeypatch.setattr(QtWidgets.QMessageBox, 'exec', lambda *args, **kwargs: QtWidgets.QMessageBox.Ok)
    qtbot.mouseClick(
        w.upd_btn,
        qt_api.QtCore.Qt.MouseButton.LeftButton
    )
    assert w.input_win is None
    assert callback.called == False

    # test one row selected:
    # press cancel
    w.table.selectRow(0)
    monkeypatch.setattr(QtWidgets.QMessageBox, 'exec', lambda *args, **kwargs: QtWidgets.QMessageBox.Cancel)
    qtbot.mouseClick(
        w.upd_btn,
        qt_api.QtCore.Qt.MouseButton.LeftButton
    )
    assert isinstance(w.input_win, InputExpenseWindow)
    assert callback.called == False
    w.input_win.close()

    # press ok
    w.table.selectRow(0)
    qtbot.mouseClick(
        w.upd_btn,
        qt_api.QtCore.Qt.MouseButton.LeftButton
    )
    assert isinstance(w.input_win, InputExpenseWindow)
    assert callback.called == False

    w.input_win.fill_in_default_data(def_values)
    qtbot.mouseClick(
        w.input_win.save_btn,
        qt_api.QtCore.Qt.MouseButton.LeftButton
    )
    assert callback.called == True
    assert callback.args[0] == '1'
    assert callback.args[1] == def_values

    w.close()

def test_del_callback_mtg(qtbot, monkeypatch):
    w = MainTableWidget(None)
    qtbot.addWidget(w)
    w.set_data(user_data)
    w.set_categories(ctg_options)

    callback = CallbackChecker()
    w.register_remove_callback(callback.check_callback)

    # test delete no selected items
    monkeypatch.setattr(QtWidgets.QMessageBox, 'exec', lambda *args, **kwargs: QtWidgets.QMessageBox.Ok)

    qtbot.mouseClick(
        w.del_btn,
        qt_api.QtCore.Qt.MouseButton.LeftButton
    )
    assert callback.called == False

    # test delete one selected items
    w.table.selectRow(0)
    # cancel
    monkeypatch.setattr(QtWidgets.QMessageBox, 'exec', lambda *args, **kwargs: QtWidgets.QMessageBox.Cancel)

    qtbot.mouseClick(
        w.del_btn,
        qt_api.QtCore.Qt.MouseButton.LeftButton
    )
    assert callback.called == False 

    w.table.selectRow(0)
    # yes
    monkeypatch.setattr(QtWidgets.QMessageBox, 'exec', lambda *args, **kwargs: QtWidgets.QMessageBox.Yes)

    qtbot.mouseClick(
        w.del_btn,
        qt_api.QtCore.Qt.MouseButton.LeftButton
    )
    assert callback.called == True
    assert callback.args[0] == [user_data[0][0]]

    w.close()

