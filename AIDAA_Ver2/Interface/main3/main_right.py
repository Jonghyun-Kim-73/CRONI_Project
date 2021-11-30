import os
import sys

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath(".."), relative_path)

source1 = resource_path("../interface/img/back.png")

class MainRight(QWidget):
    qss = """
        QWidget {
            background: rgb(231, 231, 234);
            border: 1px solid rgb(128,128,128);
            border-radius:3px;
            font-size: 14pt;
            margin:5px;
        }
        QPushButton#title{
            background: rgb(128,128,128);
            color: Black;
            border-radius:3px;
            Text-align:left;
            padding: 5px;
            padding-left:10px;
            margin:1px;
        }
        QPushButton#content{
            background: rgb(178,178,178);
            color: Black;
            border-radius:3px;
        }
        QPushButton#bottom{
            background: White;
            color: Black;
            border-radius:3px;
        }
    """

    def __init__(self, parent=None):
        super(MainRight, self).__init__()
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.layout = QVBoxLayout()

        pic = QPushButton()
        pic.setIcon(QIcon(source1))
        pic.setStyleSheet("border:0px")
        pic.setIconSize(QSize(1900, 1000))
        self.layout.addWidget(pic)

        self.setLayout(self.layout)
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainRight()
    font = QFontDatabase()
    font.addApplicationFont('./Arial.ttf')
    app.setFont(QFont('Arial'))
    window.show()
    app.exec_()
