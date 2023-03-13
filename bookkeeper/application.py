import sys

from PySide6.QtWidgets import QApplication
from bookkeeper.presenter import Bookkeeper
from bookkeeper.view.pyqt6_view import PyQtView
from bookkeeper.repository.sqlite_repository import SQLiteRepository


if __name__ == '__main__':
    app = QApplication(sys.argv)
    view = PyQtView()
    bookkeeper = Bookkeeper(view, SQLiteRepository)
    app.exec()
