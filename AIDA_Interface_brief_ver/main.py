import sys
from PyQt5.QtWidgets import *

from Old.OLD_V0.main_window import Mainwindow


class StartPoint(QWidget):
    def __init__(self):
        super(StartPoint, self).__init__()
        self.setWindowTitle("Dummy Interface")
        # initial window size
        self.setGeometry(100, 100, 200, 200)

        # initial frame
        main_window_layout = QVBoxLayout()
        main_window_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(main_window_layout)

        # showMainWindow
        Connect_btn_to_mainwindow = QPushButton('AIDAA')
        Connect_btn_to_mainwindow.clicked.connect(self._show_main_window)

        # warp up
        main_window_layout.addWidget(Connect_btn_to_mainwindow)

        self.main_window = None

        self.show()

    def _show_main_window(self):
        if self.main_window is None:
            self.main_window = Mainwindow(self)
            self.main_window.show()
        else:
            self.main_window = None


if __name__ == '__main__':
    print('test')
    app = QApplication(sys.argv)
    window = StartPoint()
    window.show()
    app.exec_()