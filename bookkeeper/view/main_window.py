""" Module for main window widgets"""
from PySide6 import QtWidgets, QtCore


class MainWindow(QtWidgets.QMainWindow):
    """ Main window class """

    def __init__(self, parent: QtWidgets.QWidget | None = None) -> None:
        super().__init__(parent=parent)

        self.setWindowTitle("Bookkeeper Application")
        self.adjust_window_to_screen()

        self.my_layout = QtWidgets.QVBoxLayout()

        self.widget = QtWidgets.QWidget()
        self.widget.setLayout(self.my_layout)
        self.setCentralWidget(self.widget)

    def set_widgets(self,
                    exp_wgt: QtWidgets.QWidget,
                    cat_wgt: QtWidgets.QWidget,
                    bgt_wgt: QtWidgets.QWidget) -> None:
        self.my_layout.addWidget(bgt_wgt, stretch=2)
        self.my_layout.addWidget(exp_wgt, stretch=5)
        self.my_layout.addWidget(cat_wgt, stretch=1)

    def adjust_window_to_screen(self) -> None:
        """ Adjust window size in correspondence with screen size"""
        w = self.screen().geometry().width()
        h = self.screen().geometry().height()

        self.resize(QtCore.QSize(int(0.5*w), int(0.5*h)))
        self.setGeometry(int(0.25*w), int(0.25*h), int(0.5*w), int(0.5*h))
        self.setMinimumSize(QtCore.QSize(int(0.25*w), int(0.25*h)))
        self.setMaximumSize(QtCore.QSize(int(0.75*w), int(0.75*h)))
