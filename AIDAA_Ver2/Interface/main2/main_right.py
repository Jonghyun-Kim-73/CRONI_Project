import sys

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

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
        self.parent = parent
        self.setStyleSheet(self.qss)
        # self.setFixedWidth(1500)
        # 기본 속성
        # self.setMinimumHeight(750)

        # 레이아웃
        layout = QVBoxLayout(self)
        layout_title = QHBoxLayout(self)
        title_btn = []
        title_item_list = ["2.0 경보 및 증상", "VALUE", "SETPOINT", "UNIT", ""]
        for cnt in title_item_list:
            title_btn.append(QPushButton(cnt))
        for cnt in range(len(title_item_list)):
            title_btn[cnt].setObjectName("title")
            layout_title.addWidget(title_btn[cnt])
        title_btn[0].setFixedWidth(840)
        title_btn[1].setFixedWidth(180)
        title_btn[2].setFixedWidth(170)
        title_btn[3].setFixedWidth(160)
        title_btn[4].setFixedWidth(40)
        layout_title.addStretch(1)
        layout_title.setContentsMargins(10,0,10,0)
        layout.addLayout(layout_title)
        layout.addStretch(1)
        self.setLayout(layout)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainRight()
    font = QFontDatabase()
    font.addApplicationFont('./Arial.ttf')
    app.setFont(QFont('Arial'))
    window.show()
    app.exec_()
