import sys
from functools import partial

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from AIDAA_Ver2.Interface import Flag


class MainLeft(QWidget):
    qss = """
        QWidget {
            background: rgb(231, 231, 234);
            border: 0px solid rgb(0, 0, 0); 
            font-size: 14pt;
        }
        QPushButton{
            background: White;
            color: Black;
            border-radius:3px;
            padding:5px;
            font-size: 14pt;
            Text-align:left;
            padding-left:10px;
            margin-bottom:10px;
        }
        QHeaderView::section {
            padding-left: 15px; 
            border: 0px;
        }
    """

    def __init__(self, parent = None):
        super(MainLeft, self).__init__()
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.parent = parent
        self.setStyleSheet(self.qss)
        # self.setFixedWidth(990)
        # 기본 속성
        # self.setMinimumHeight(750)

        # 레이아웃
        layout = QVBoxLayout(self)

        # 변수 받아와야함
        item_list = ["2.0 경보 및 증상 [3/4]", "3.0 자동 동작 사항 [3/5]", "4.0 긴급 조치 사항 [3/5]", "5.0 후속 조치 사항 [3/5]"]

        btn = []
        for item in item_list:
            btn.append(QPushButton(item))
        for cnt in range(len(item_list)):
            btn[cnt].setFixedWidth(450)
            btn[cnt].clicked.connect(partial(self.click, cnt))
            layout.addWidget(btn[cnt])
        layout.addStretch(1)
        self.setLayout(layout)

    def click(self, btn_num):
        Flag.main2_btn[btn_num] = True
        print("클릭함", btn_num)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainLeft()
    font = QFontDatabase()
    font.addApplicationFont('./Arial.ttf')
    app.setFont(QFont('Arial'))
    window.show()
    app.exec_()
