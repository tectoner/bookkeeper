import itertools
from functools import partial

from PySide6 import QtWidgets, QtGui, QtCore
from typing import Callable


class InputExpenseWindow(QtWidgets.QDialog):
    """ Window for entering information about new expense """

    def __init__(
        self,
        parent: QtWidgets.QWidget | None,
        on_clicked_save_callback: Callable[[dict[str, str]], None],
        ctg_options: list[str],
        msg_dict: dict[str, str],
        default_values: dict[str, str] | None = None
    ):
        super().__init__(parent)

        self.msg_dict = msg_dict
        if (self.msg_dict.get('window_title') is None or
                self.msg_dict.get('save_button_text') is None):
            raise KeyError('No <window_title> or <save_button_text>')

        self.setWindowTitle(msg_dict['window_title'])

        self.on_clicked_save_callback = on_clicked_save_callback
        self.ctg_options = ctg_options

        self.my_layout = QtWidgets.QVBoxLayout()
        self.expense_date: QtWidgets.QDateEdit
        self.amount: QtWidgets.QLineEdit
        self.category: QtWidgets.QComboBox
        self.comment: QtWidgets.QLineEdit

        self.create_widgets()

        if not default_values is None:
            self.fill_in_default_data(default_values)

        self.save_btn = QtWidgets.QPushButton(msg_dict['save_button_text'])
        self.save_btn.clicked.connect(self._on_clicked_save_btn)
        self.my_layout.addWidget(self.save_btn)

        self.setLayout(self.my_layout)

    def fill_in_default_data(self, data: dict[str, str]) -> None:
        self.expense_date.setDate(
            QtCore.QDate.fromString(f"{data['expense_date']}", 'dd-MM-yyyy')
        )
        self.expense_date.show()
        self.amount.setText(f"{float(data['amount']):.2f}")
        self.category.setCurrentText(f"{data['category']}")
        self.comment.setText(f"{data['comment']}")

    def create_widgets(self) -> None:
        """ Create widgets and add them to layout"""
        label = QtWidgets.QLabel('Дата покупки')
        self.my_layout.addWidget(label)

        self.expense_date = QtWidgets.QDateEdit()
        self.expense_date.setDisplayFormat('dd-MM-yyyy')
        self.expense_date.setMinimumDate(
            QtCore.QDate.fromString('01-01-2022', 'dd-MM-yyyy'))
        self.expense_date.setMaximumDate(
            QtCore.QDate.fromString('01-01-2100', 'dd-MM-yyyy'))
        self.my_layout.addWidget(self.expense_date)

        label = QtWidgets.QLabel('Сумма покупки (руб.)')
        self.my_layout.addWidget(label)
        self.amount = QtWidgets.QLineEdit()
        self.amount.setPlaceholderText('500')
        self.amount.setValidator(QtGui.QDoubleValidator(0, 1000000, 2))
        self.my_layout.addWidget(self.amount)

        label = QtWidgets.QLabel('Категория покупки')
        self.my_layout.addWidget(label)
        self.category = QtWidgets.QComboBox()
        self.category.setPlaceholderText('Выбрать')
        self.category.addItems(self.ctg_options)
        self.my_layout.addWidget(self.category)

        label = QtWidgets.QLabel('Комментарий')
        self.my_layout.addWidget(label)
        self.comment = QtWidgets.QLineEdit()
        self.comment.setPlaceholderText('Кафе после работы')
        self.my_layout.addWidget(self.comment)

    def _is_mandatory_filled(self) -> bool:
        """ Check if mandatory fields are filled"""
        return bool(self.amount.text() and self.category.currentText())

    def get_data(self) -> dict[str, str]:
        """ Get formatted data"""
        return {
            'expense_date': self.expense_date.date().toString('dd-MM-yyyy'),
            'amount': self.amount.text(),
            'category': self.category.currentText(),
            'comment': self.comment.text()
        }

    def _on_clicked_save_btn(self) -> None:
        """ Reaction on clicked save button """
        if self._is_mandatory_filled():
            self.on_clicked_save_callback(self.get_data())
            self.close()
        else:
            dlg = QtWidgets.QMessageBox(
                parent=self,
                icon=QtWidgets.QMessageBox.Information,
                text="Заполните поля 'сумма' и 'категория'"
            )
            dlg.setWindowTitle(' ')
            dlg.setStandardButtons(QtWidgets.QMessageBox.Ok)
            dlg.exec()


class MainTableWidget(QtWidgets.QWidget):
    """ Main widget for displaying expense table"""
    user_data = list[list[str]]
    update_callback: Callable[[str, dict[str, str]], None]
    remove_callback: Callable[[list[str]], None]
    add_callback: Callable[[dict[str, str]], None]
    input_win: InputExpenseWindow | None

    def __init__(self, parent: QtWidgets.QWidget | None = None):
        super().__init__(parent=parent)

        self.table = QtWidgets.QTableWidget()
        self.set_up_table()
        self.input_win = None

        self.add_btn = QtWidgets.QPushButton("Добавить")
        self.add_btn.clicked.connect(self._on_clicked_add_button)
        self.del_btn = QtWidgets.QPushButton("Удалить")
        self.del_btn.clicked.connect(self._on_clicked_del_button)
        self.upd_btn = QtWidgets.QPushButton("Редактировать")
        self.upd_btn.clicked.connect(self._on_clicked_upd_button)

        # horizontal layout with buttons
        v_layout1 = QtWidgets.QVBoxLayout()
        for btn in [self.add_btn, self.del_btn, self.upd_btn]:
            v_layout1.addWidget(btn)

        # buttons under the table
        v_layout2 = QtWidgets.QVBoxLayout()
        v_layout3 = QtWidgets.QVBoxLayout()
        
        v_layout2.addWidget(QtWidgets.QLabel("Мои последние расходы"),
                           alignment=QtCore.Qt.AlignmentFlag.AlignCenter)
        v_layout2.addWidget(self.table)
        v_layout3.addWidget(QtWidgets.QLabel("Управление записями"),
                           alignment=QtCore.Qt.AlignmentFlag.AlignCenter)
        v_layout3.addLayout(v_layout1)

        h_layout = QtWidgets.QHBoxLayout()
        h_layout.addLayout(v_layout2)
        h_layout.addLayout(v_layout3)

        self.setLayout(h_layout)

    def _on_clicked_upd_button(self) -> None:
        idx = self.table.selectedItems()
        rows = list(set([i.row() for i in idx]))

        msg_dict = {
            'window_title': 'Редактировать запись',
            'save_button_text': 'Сохранить изменения'
        }

        if len(rows) == 0:
            dlg = QtWidgets.QMessageBox(
                parent=self,
                icon=QtWidgets.QMessageBox.Information,
                text="Выберете запись для редактирования."
            )
            dlg.setWindowTitle(' ')
            dlg.setStandardButtons(QtWidgets.QMessageBox.Ok)
            dlg.exec()

        elif len(rows) == 1:
            sel_row = rows[0]
            pk = self.user_data[sel_row][0]
            row_data = {
                'expense_date': self.user_data[sel_row][1], 'amount': self.user_data[sel_row][2],
                'category': self.user_data[sel_row][3], 'comment': self.user_data[sel_row][4]
            }
            self.input_win = InputExpenseWindow(
                self,
                on_clicked_save_callback=partial(self.update_callback, pk),
                ctg_options=self.cat_data,
                msg_dict=msg_dict,
                default_values=row_data
            )
            self.input_win.show()
        else:
            dlg = QtWidgets.QMessageBox(
                parent=self,
                icon=QtWidgets.QMessageBox.Information,
                text="За раз можно отредактировать только одну запись."
            )
            dlg.setWindowTitle(' ')
            dlg.setStandardButtons(QtWidgets.QMessageBox.Ok)
            dlg.exec()

    def _on_clicked_add_button(self) -> None:

        msg_dict = {
            'window_title': 'Добавление новой записи',
            'save_button_text': 'Добавить'
        }
        self.input_win = InputExpenseWindow(
            self,
            on_clicked_save_callback=self.add_callback,
            ctg_options=self.cat_data,
            msg_dict=msg_dict
        )
        self.input_win.show()

    def _on_clicked_del_button(self) -> None:
        idx = self.table.selectedItems()
        if len(idx) == 0:
            dlg = QtWidgets.QMessageBox(
                parent=self,
                icon=QtWidgets.QMessageBox.Information,
                text="Выберите записи в таблице расходов"
            )
            dlg.setWindowTitle(' ')
            dlg.setStandardButtons(QtWidgets.QMessageBox.Ok)
            dlg.exec()
        else:
            dlg = QtWidgets.QMessageBox(
                parent=self,
                icon=QtWidgets.QMessageBox.Question,
                text="Удалить записи?"
            )
            dlg.setWindowTitle('Удаление категории')
            dlg.setStandardButtons(QtWidgets.QMessageBox.Yes |
                                   QtWidgets.QMessageBox.Cancel)
            answer = dlg.exec()

            if answer == QtWidgets.QMessageBox.Yes:
                rows = set([i.row() for i in idx])
                pks = [self.user_data[i][0] for i in rows]
                self.remove_callback(pks)

    def register_add_callback(self, callback: Callable[[dict[str, str]], None]) -> None:
        self.add_callback = callback

    def register_remove_callback(self, callback: Callable[[list[str]], None]) -> None:
        self.remove_callback = callback

    def register_update_callback(self, callback: Callable[[str, dict[str, str]], None]) -> None:
        self.update_callback = callback

    def set_categories(self, cat_data: list[str]) -> None:
        self.cat_data = cat_data

    def set_data(self, user_data: list[list[str]]) -> None:
        """
        Set user data to be displayed.
        The first element in each row is considered as a primary
        and is not displayed.
        Primary key is used in callbacks.
        """
        self.user_data = user_data
        self.table.setRowCount(len(self.user_data))

        n_cols = self.table.columnCount()
        n_rows = self.table.rowCount()

        for row, col in itertools.product(range(n_rows), range(n_cols)):
            item = QtWidgets.QTableWidgetItem(self.user_data[row][col+1])
            item.setFlags(
                QtCore.Qt.ItemFlag.ItemIsSelectable |
                QtCore.Qt.ItemFlag.ItemIsEnabled)

            self.table.setItem(row, col, item)

    def set_up_table(self) -> None:
        my_headers = ['Дата покупки', 'Сумма, руб.', 'Категория', 'Комментарий']
        self.table.setColumnCount(len(my_headers))
        self.table.setHorizontalHeaderLabels(my_headers)

        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(
            len(my_headers)-1, QtWidgets.QHeaderView.ResizeMode.Stretch)
