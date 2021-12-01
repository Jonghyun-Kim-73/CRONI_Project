import os
import sys
from datetime import datetime

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from AIDAA_Ver2.Interface import Flag


def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath(""), relative_path)

class MainTop2(QComboBox):
    qss = """
        QComboBox{
            background: white;
            border: 0px solid rgb(0, 0, 0); 
            border-radius: 3px;
            color: black;
            font-size: 14pt;
            padding: 5px 0px 5px 10px;
        }
        QListView{
            background-color: white;
        }
        QComboBox::drop-down 
        {
            width: 40px; 
            border: 0px; 
        }
        QComboBox::down-arrow {
            image: url(../interface/img/down.png);
            top: 3px;
            width: 60px;
            height: 60px;
        }
        """

    def __init__(self, parent=None):
        super(MainTop2, self).__init__()
        self.setStyleSheet(self.qss)
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setFixedHeight(45)
        list = ["비정상절차서: 가압기 압력 채널 고장 (고)", "추가 1", "추가 2", "추가 3"]
        self.addItems(list)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainTop2()
    window.show()
    font = QFontDatabase()
    font.addApplicationFont('./Arial.ttf')
    app.setFont(QFont('Arial'))
    app.exec_()