import sys

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


class Main2Prog(QWidget):
    qss = """
        QWidget {
            background: rgb(231, 231, 234);
            border: 0px solid rgb(0, 0, 0); 
            font-size: 14pt;
        }
        QLabel#title{
            background: rgb(128, 128, 128);
            padding:10px;
            border-radius:5px;
        }
        QTextEdit{
            background: rgb(178, 178, 178);
            border-radius:5px;
            height:30px;
        }
    """

    def __init__(self, parent = None):
        super(Main2Prog, self).__init__()
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.parent = parent
        self.setStyleSheet(self.qss)
        # self.setFixedWidth(990)
        # 기본 속성
        # self.setMinimumHeight(750)

        # 레이아웃
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        g1 = Graph1(self)
        g2 = Graph2(self)
        g3 = Graph3(self)
        g4 = Graph4(self)

        layout.addWidget(g1)
        layout.addWidget(g2)
        layout.addWidget(g3)
        layout.addWidget(g4)

        self.setLayout(layout)

class Graph1(QGroupBox):
    def __init__(self, parent=None):
        super(Graph1, self).__init__()
        self.setAttribute(Qt.WA_StyledBackground, True)

        layout = QVBoxLayout(self)
        self.setFixedWidth(200)
        self.title = QLabel("변수 명")
        self.title.setFixedHeight(40)
        self.title.setObjectName("title")

        self.text = []
        for i in range(10):
            self.text.append(QTextEdit())
        self.text[0].setText("선원 영역")
        self.text[1].setText("중간 영역")
        self.text[2].setText("출력 영역")
        self.text[3].setText("OT△T 트립")
        self.text[4].setText("OP△T 트립")
        self.text[5].setText("가압기 압력")
        self.text[6].setText("가압기 수위")
        self.text[7].setText("S/G 수위")
        self.text[8].setText("격납용기 압력")
        self.text[9].setText("주증기관 압력")

        layout.addWidget(self.title)
        layout.addStretch(1)
        for i in range(10):
            self.text[i].setFixedHeight(40)
            self.text[i].setAlignment(Qt.AlignVCenter)
            layout.addWidget(self.text[i])
            layout.addStretch(1)
        self.setLayout(layout)

class Graph2(QGroupBox):
    def __init__(self, parent=None):
        super(Graph2, self).__init__()
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setFixedWidth(200)
        layout = QVBoxLayout(self)

        self.title = QLabel("Trip 도달 시간")
        self.title.setFixedHeight(40)
        self.title.setObjectName("title")

        self.text = []
        for i in range(10):
            self.text.append(QTextEdit("시간"))

        layout.addWidget(self.title)
        layout.addStretch(1)
        for i in range(10):
            self.text[i].setFixedHeight(40)
            self.text[i].setAlignment(Qt.AlignVCenter)
            layout.addWidget(self.text[i])
            layout.addStretch(1)

        self.setLayout(layout)

class Graph3(QGroupBox):
    def __init__(self, parent=None):
        super(Graph3, self).__init__()
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setFixedWidth(200)
        layout = QVBoxLayout(self)

        self.title = QLabel("단축(min)")
        self.title.setObjectName("title")
        # self.text1 = QTextEdit("시간")
        # self.text2 = QTextEdit("시간")
        # self.text3 = QTextEdit("시간")
        # self.text4 = QTextEdit("시간")
        # self.text5 = QTextEdit("시간")
        # self.text6 = QTextEdit("시간")
        # self.text7 = QTextEdit("시간")
        # self.text8 = QTextEdit("시간")
        # self.text9 = QTextEdit("시간")
        # self.text10 = QTextEdit("시간")

        layout.addWidget(self.title)
        # layout.addWidget(self.text1)
        # layout.addWidget(self.text2)
        # layout.addWidget(self.text3)
        # layout.addWidget(self.text4)
        # layout.addWidget(self.text5)
        # layout.addWidget(self.text6)
        # layout.addWidget(self.text7)
        # layout.addWidget(self.text8)
        # layout.addWidget(self.text9)
        # layout.addWidget(self.text10)
        layout.addStretch(1)
        self.setLayout(layout)

class Graph4(QGroupBox):
    def __init__(self, parent=None):
        super(Graph4, self).__init__()
        self.setAttribute(Qt.WA_StyledBackground, True)

        layout = QVBoxLayout(self)

        self.title = QLabel("장축(min)")
        self.title.setObjectName("title")
        self.title.setAlignment(Qt.AlignCenter)
        # self.text1 = QTextEdit("시간")
        # self.text2 = QTextEdit("시간")
        # self.text3 = QTextEdit("시간")
        # self.text4 = QTextEdit("시간")
        # self.text5 = QTextEdit("시간")
        # self.text6 = QTextEdit("시간")
        # self.text7 = QTextEdit("시간")
        # self.text8 = QTextEdit("시간")
        # self.text9 = QTextEdit("시간")
        # self.text10 = QTextEdit("시간")

        layout.addWidget(self.title)
        # layout.addWidget(self.text1)
        # layout.addWidget(self.text2)
        # layout.addWidget(self.text3)
        # layout.addWidget(self.text4)
        # layout.addWidget(self.text5)
        # layout.addWidget(self.text6)
        # layout.addWidget(self.text7)
        # layout.addWidget(self.text8)
        # layout.addWidget(self.text9)
        # layout.addWidget(self.text10)
        layout.addStretch(1)
        self.setLayout(layout)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Main2Prog()
    font = QFontDatabase()
    font.addApplicationFont('./Arial.ttf')
    app.setFont(QFont('Arial'))
    window.show()
    app.exec_()