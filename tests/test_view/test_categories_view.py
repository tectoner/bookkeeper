from pytestqt.qt_compat import qt_api
import pytestqt

from PySide6 import QtWidgets

from bookkeeper.view.categories_view import EditCategoriesWindow, MainCategoryWidget

class CallbackChecker():
    def __init__(self):
        self.called = False
        self.args = None
        self.kwargs = None

    def check_callback(self, *args, **kwargs):
        self.called = True
        self.args = args
        self.kwargs = kwargs


def test_create_ecw(qtbot):

    user_data = [['1', 'A'], ['2', 'B']]

    add_callback_checker = CallbackChecker()
    del_callback_checker = CallbackChecker()

    window = EditCategoriesWindow(parent=None,
                                  data=user_data,
                                  add_callback=add_callback_checker.check_callback,
                                  del_callback=del_callback_checker.check_callback)
    qtbot.addWidget(window)

    assert window.user_data == user_data
    assert window.add_callback == add_callback_checker.check_callback
    assert window.del_callback == del_callback_checker.check_callback
    assert window.ctgs_lst == ['A', 'B']


    window.set_data(user_data)
    assert window.user_data == user_data

    #ctgs widget
    assert window.ctg_lst_widget.count() == 2
    assert window.ctg_lst_widget.item(0).text() == 'A'
    assert window.ctg_lst_widget.item(1).text() == 'B'

def test_add_btns_ecw(qtbot, monkeypatch):

    user_data = [['1', 'A'], ['2', 'B']]

    callback_checker = CallbackChecker()

    window = EditCategoriesWindow(parent=None,
                                  data=user_data,
                                  add_callback=callback_checker.check_callback,
                                  del_callback=lambda x: x)
    qtbot.addWidget(window)

    # callback doesn't trigger on cancel
    callback_checker.called = False
    monkeypatch.setattr(QtWidgets.QMessageBox, 'exec', lambda *args, **kwargs: QtWidgets.QMessageBox.Cancel)
    window.add_input.setText('new category')
    qtbot.mouseClick(
        window.add_btn,
        qt_api.QtCore.Qt.MouseButton.LeftButton
    )

    assert callback_checker.called == False

    # callback triggers on ok
    callback_checker.called = False
    monkeypatch.setattr(QtWidgets.QMessageBox, 'exec', lambda *args, **kwargs: QtWidgets.QMessageBox.Yes)
    window.add_input.setText('new category')
    qtbot.mouseClick(
        window.add_btn,
        qt_api.QtCore.Qt.MouseButton.LeftButton
    )

    assert callback_checker.called == True
    assert callback_checker.args[0] == 'new category'
    assert len(callback_checker.args) == 1

def test_del_btns_ecw(qtbot, monkeypatch):

    user_data = [['1', 'A'], ['2', 'B']]

    callback_checker = CallbackChecker()

    window = EditCategoriesWindow(parent=None,
                                  data=user_data,
                                  del_callback=callback_checker.check_callback,
                                  add_callback=lambda x: x)
    qtbot.addWidget(window)


    # callback doesn't trigger on cancel
    callback_checker.called = False
    monkeypatch.setattr(QtWidgets.QMessageBox, 'exec', lambda *args, **kwargs: QtWidgets.QMessageBox.Cancel)
    window.del_input.setCurrentIndex(0)
    qtbot.mouseClick(
        window.del_btn,
        qt_api.QtCore.Qt.MouseButton.LeftButton
    )

    assert callback_checker.called == False

    # callback triggers on yes
    callback_checker.called = False
    monkeypatch.setattr(QtWidgets.QMessageBox, 'exec', lambda *args, **kwargs: QtWidgets.QMessageBox.Yes)
    window.del_input.setCurrentIndex(0)
    qtbot.mouseClick(
        window.del_btn,
        qt_api.QtCore.Qt.MouseButton.LeftButton
    )

    assert callback_checker.called == True
    assert callback_checker.args[0] == '1'
    assert len(callback_checker.args) == 1

def test_create_mcw(qtbot):

    window = MainCategoryWidget()
    qtbot.addWidget(window)

    user_data = [['1', 'A'], ['2', 'B']]
    callback_checker_1 = CallbackChecker()
    callback_checker_2 = CallbackChecker()

    window.register_add_callback(callback_checker_1)
    window.register_del_callback(callback_checker_2)
    window.set_data(user_data)

    assert window.edit_window is None
    assert window.add_callback == callback_checker_1
    assert window.del_callback == callback_checker_2
    assert window.user_data == user_data

def test_edit_mcw(qtbot):
    window = MainCategoryWidget()
    qtbot.addWidget(window)

    user_data = [['1', 'A'], ['2', 'B']]
    callback_checker_1 = CallbackChecker()
    callback_checker_2 = CallbackChecker()

    window.register_add_callback(callback_checker_1)
    window.register_del_callback(callback_checker_2)
    window.set_data(user_data)

    assert window.edit_window is None
    qtbot.mouseClick(
        window.btn,
        qt_api.QtCore.Qt.MouseButton.LeftButton
    )
    assert not window.edit_window is None

    window.edit_window.close()

