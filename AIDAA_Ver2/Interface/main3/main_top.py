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
    return os.path.join(os.path.abspath(".."), relative_path)

source1 = resource_path("../interface/img/return.png")
source2 = resource_path("../interface/img/close.png")

class MainTop(QWidget):
    qss = """
        QWidget {
            background: rgb(128, 128, 128);
            border: 0px solid rgb(0, 0, 0); 
            border-radius: 3px;
        }
        QPushButton#main1{
            background: rgb(0, 176, 218);
            font-size: 14pt;
            color: rgb(0, 0, 0);
        }
        QPushButton#main2{
            background: rgb(231, 231, 234);
            font-size: 14pt;
            color: rgb(0, 0, 0);
        }
        QPushButton{
            border-radius: 3px;
        }
        """

    def __init__(self, parent=None):
        super(MainTop, self).__init__()

        self.bar_height = 37
        self.setStyleSheet(self.qss)
        self.setAttribute(Qt.WA_StyledBackground, True)
        # 타이틀 레이어 셋업 ----------------------------------------------------------------------------------------------
        layout = QHBoxLayout(self)  # 수평 방향 레이아웃
        layout.setContentsMargins(5, 5, 5, 5)  # 위젯의 여백 설정

        #DayBarm TimeBar
        widget1 = TimeBar(self, load_realtime=True, load_realtime2=True)
        widget1.setFixedHeight(self.bar_height)
        widget1.setFixedWidth(380)

        #라벨 설정
        label0 = QLabel("")
        label0.setObjectName("black")
        label0.setFixedWidth(200)
        label1 = QPushButton("Main")
        label1.setObjectName('main1')

        #AlignVCenter 수직가운데정렬 / AlignHCenter 수평가운데정렬 / AlignCenter 모두 적용
        # label1.setAlignment(Qt.AlignCenter)
        label1.setFixedHeight(self.bar_height)
        label1.setFixedWidth(620)

        label2 = QPushButton("예지")
        label2.setObjectName('main2')

        # label2.setAlignment(Qt.AlignCenter)
        label2.setFixedHeight(self.bar_height)
        label2.setFixedWidth(620)

        btn_return = QPushButton()
        btn_return.setIcon(QIcon(source1))
        btn_return.setStyleSheet("border:0px")
        #btn_return.clicked.connect(self.close) #되돌아가기 기능 추가해야함
        btn_return.setIconSize(QSize(60, 60))
        btn_return.setFixedSize(30, 30)

        btn_close = QPushButton()
        btn_close.setIcon(QIcon(source2))
        btn_close.setStyleSheet("border:0px;")
        btn_close.clicked.connect(self.close)
        btn_close.setIconSize(QSize(30, 30))
        btn_close.setFixedSize(30, 30)

        layout.addWidget(widget1)
        layout.addWidget(label0)
        layout.addWidget(label1)
        layout.addWidget(label2)
        layout.addWidget(btn_return)
        layout.addWidget(btn_close)

    def close(self):
        Flag.main_close = True

class TimeBar(QWidget):
    qss = """
        QLabel{
            background: rgb(255, 255, 255);
            color: rgb(0, 0, 0);
            padding: 4px 4px;
            font-size: 14pt;
        }
    """

    def __init__(self, parent, load_realtime: bool = False, load_realtime2: bool = False):
        super(TimeBar, self).__init__()
        self.parent = parent
        self.load_realtime = load_realtime
        self.load_realtime2 = load_realtime2

        self.setObjectName('TimeBar')
        self.setStyleSheet(self.qss)

        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        self.timebarlabel = QLabel('time')
        self.timebarlabel.setAlignment(Qt.AlignCenter)  # 텍스트 정렬
        self.timebarlabel.setObjectName('TimeBarLabel')
        self.dis_update()

        layout.addWidget(self.timebarlabel)

        self.setLayout(layout)

        # timer section
        timer = QTimer(self)
        timer.setInterval(1000)
        timer.timeout.connect(self.dis_update)
        timer.start()

    def dis_update(self):
        """ 타이머 디스플레이 업데이트 """
        real_time = datetime.now().strftime('%Y.%m.%d')
        real_time2 = datetime.now().strftime('%H:%M:%S')
        self.timebarlabel.setText(real_time + " / " + real_time2)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainTop()
    window.show()
    font = QFontDatabase()
    font.addApplicationFont('./Arial.ttf')
    app.setFont(QFont('Arial'))
    app.exec_()