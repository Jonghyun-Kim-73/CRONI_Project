import sys

import numpy as np
import pandas as pd
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas



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
        self.start_x = 100
        self.start_y = 200
        self.arrow = QPolygonF([QPointF(self.start_x - 8, self.start_y),
                           QPointF(self.start_x, self.start_y - 6),
                           QPointF(self.start_x, self.start_y + 6),
                           QPointF(self.start_x - 8, self.start_y)])


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
    qss = """QGroupBox{
            border: 2px solid rgb(0, 0, 0); 
            }
        """
    def __init__(self, parent):
        super(Graph3, self).__init__(parent)
        self.setAttribute(Qt.WA_StyledBackground, True)

        self.setFixedWidth(200)
        layout = QVBoxLayout(self)

        self.title = QLabel("단축(min)")
        self.title.setObjectName("title")

        self.fig = plt.Figure()

        plt.style.use('default')
        plt.rcParams['figure.figsize'] = (2, 1)
        # plt.rcParams['font.size'] = 3

        self.fig, ax = plt.subplots()
        self.canvas = []

        # 임시 그래프 10개 생성
        for cnt in range(10):
            self.canvas.append(FigureCanvas(self.fig))

        # 임시 그래프
        ax.set_xlim(-2, 2)
        ax.set_ylim(0, 2)
        ax.set_xticks([])
        ax.set_yticks([])

        ax.spines['left'].set_position('center')  # 왼쪽 축을 가운데 위치로 이동
        ax.spines['right'].set_visible(False)  # 오른쪽 축을 보이지 않도록
        ax.spines['top'].set_visible(False)  # 위 축을 보이지 않도록
        ax.spines['bottom'].set_position(('data', 0))  # 아래 축을 데이터 0의 위치로 이동
        ax.tick_params('both', length=0)  # Tick의 눈금 길이 0

        x = np.linspace(-2, 0, 100)
        y = np.linspace(1.2, 1, 100)
        x2 = np.linspace(0, 2, 100)
        y2 = np.linspace(1, 0, 100)
        ax.plot(x, y, color='#000000', linewidth=2)
        ax.plot(x2, y2, color='#00B0DA', linewidth=2)
        self.fig.patch.set_facecolor('#E7E7EA')  # 그래프 밖 color
        ax.set_facecolor('#E7E7EA')  # 그래프 안 color

        # canvas border 설정
        rect = plt.Rectangle(
            # (lower-left corner), width, height
            (0.02, 0.02), 0.95, 0.9, fill=False, color="k", lw=0.5, alpha=0.5,
            zorder=1000, transform=self.fig.transFigure, figure=self.fig
        )
        self.fig.patches.extend([rect])
        plt.tight_layout()

        layout.addWidget(self.title)

        for cnt in range(10):
            layout.addWidget(self.canvas[cnt])
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

        self.fig = plt.Figure()
        plt.style.use('default')
        plt.rcParams['figure.figsize'] = (13, 1)
        # plt.rcParams['font.size'] = 3
        self.fig, ax = plt.subplots()
        self.canvas = []

        # 임시 그래프 10개 생성
        for cnt in range(10):
            self.canvas.append(FigureCanvas(self.fig))

        # 임시 그래프
        ax.set_xlim(-2, 120)
        ax.set_ylim(0, 2)
        ax.set_xticks([])
        ax.set_yticks([])

        ax.spines['left'].set_position(('data', 0))  # 왼쪽 축을 데이터 0의 위치로 이동
        ax.spines['right'].set_visible(False)  # 오른쪽 축을 보이지 않도록
        ax.spines['top'].set_visible(False)  # 위 축을 보이지 않도록
        ax.spines['bottom'].set_position(('data', 0))  # 아래 축을 데이터 0의 위치로 이동
        ax.tick_params('both', length=0)  # Tick의 눈금 길이 0

        x = np.linspace(-2, 0, 120)
        y = np.linspace(1.2, 1, 120)
        x2 = np.linspace(0, 2, 120)
        y2 = np.linspace(1, 0, 120)
        ax.plot(x, y, color='#000000', linewidth=2)
        ax.plot(x2, y2, color='#00B0DA', linewidth=2)
        self.fig.patch.set_facecolor('#E7E7EA')  # 그래프 밖 color
        ax.set_facecolor('#E7E7EA')  # 그래프 안 color

        # canvas border 설정
        rect = plt.Rectangle(
            # (lower-left corner), width, height
            (0.005, 0.02), 0.99, 0.9, fill=False, color="k", lw=0.5, alpha=0.5,
            zorder=1000, transform=self.fig.transFigure, figure=self.fig
        )
        self.fig.patches.extend([rect])
        plt.tight_layout()
        layout.addWidget(self.title)

        for cnt in range(10):
            layout.addWidget(self.canvas[cnt])
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