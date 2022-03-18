import os
import sys
from datetime import datetime

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from AIDAA_Ver2.Interface import Flag
from AIDAA_Ver2.TOOL.TOOL_etc import p_
from AIDAA_Ver2.TOOL.TOOL_Shmem import SHMem
from AIDAA_Ver2.TOOL.TOOL_Widget import *

ROOT_PATH = os.path.dirname(os.path.abspath(__file__))


class MainTop(ABCWidget):
    qss = """
        QWidget {
            background: rgb(128, 128, 128);
            border: 0px solid rgb(0, 0, 0);
            border-radius: 6px;
        }
        QPushButton#main1{
            background: rgb(231, 231, 234);
            font-size: 14pt;
            color: rgb(0, 0, 0);
            border-radius: 6px;
        }
        QPushButton#main2{
            background: rgb(231, 231, 234);
            font-size: 14pt;
            color: rgb(0, 0, 0);
            border-radius: 6px;
        }
        QPushButton{
            border-radius: 6px;
        }
        """

    def __init__(self, parent, bar_height=35):
        super(MainTop, self).__init__(parent)
        self.bar_height = bar_height
        self.setStyleSheet(self.qss)

        # 타이틀 레이어 셋업 ----------------------------------------------------------------------------------------------
        layout = WithNoMargin(QHBoxLayout(self), c_m=5)  # 수평 방향 레이아웃

        #DayBarm TimeBar
        widget1 = TimeBar(self, h=bar_height, w=380)
        widget1.setFixedHeight(self.bar_height)
        widget1.setFixedWidth(380)

        #라벨 설정
        label0 = QLabel("")
        label0.setObjectName("black")
        label0.setFixedWidth(200)

        self.label1 = QPushButton("Main")
        self.label1.setObjectName('main1')
        self.label1.setStyleSheet('background: rgb(24, 144, 255);')
        self.label1.clicked.connect(self.call_main)

        # AlignVCenter 수직가운데정렬 / AlignHCenter 수평가운데정렬 / AlignCenter 모두 적용
        # label1.setAlignment(Qt.AlignCenter)
        self.label1.setFixedHeight(self.bar_height)
        self.label1.setFixedWidth(620)

        self.label2 = QPushButton("예지")
        self.label2.setObjectName('main2')
        self.label2.clicked.connect(self.call_prog)

        # label2.setAlignment(Qt.AlignCenter)
        self.label2.setFixedHeight(self.bar_height)
        self.label2.setFixedWidth(620)

        btn_return = ReturnBTN(self)
        btn_close = CloseBTN(self)

        layout.addWidget(widget1)
        layout.addWidget(label0)
        layout.addWidget(self.label1)
        layout.addWidget(self.label2)
        layout.addWidget(btn_return)
        layout.addWidget(btn_close)

        timer = QTimer(self)
        timer.setInterval(300)
        timer.timeout.connect(self.call_page)
        timer.start()

    def call_page(self):
        if Flag.return_page == 0:
            self.label1.setStyleSheet('background: rgb(24, 144, 255);')
            self.label2.setStyleSheet('background: rgb(231, 231, 234);')
            Flag.return_page = -1
        elif Flag.return_page == 1:
            self.label1.setStyleSheet('background: rgb(231, 231, 234);')
            self.label2.setStyleSheet('background: rgb(24, 144, 255);')
            Flag.return_page = -1

    def call_main(self):
        Flag.call_main = True
        Flag.return_list.append("Main")
        self.label1.setStyleSheet('background: rgb(24, 144, 255);')
        self.label2.setStyleSheet('background: rgb(231, 231, 234);')

    def call_prog(self):
        Flag.call_prog = True
        Flag.return_list.append("예지")
        self.label1.setStyleSheet('background: rgb(231, 231, 234);')
        self.label2.setStyleSheet('background: rgb(24, 144, 255);')


class TimeBar(QWidget):
    qss = """
        QLabel{
            background: rgb(255, 255, 255);
            color: rgb(0, 0, 0);
            padding: 4px 4px;
            border-radius: 6px;
            font-size: 14pt;
        }
    """

    def __init__(self, parent, h, w):
        super(TimeBar, self).__init__()
        self.parent = parent
        self.setStyleSheet(self.qss)
        self.setFixedWidth(w)
        self.setFixedHeight(h)

        self.timebarlabel = QLabel('time')
        self.timebarlabel.setAlignment(Qt.AlignCenter)  # 텍스트 정렬
        self.timebarlabel.setObjectName('TimeBarLabel')

        layout = WithNoMargin(QHBoxLayout(self))
        layout.addWidget(self.timebarlabel)

        # timer section
        timer = QTimer(self)
        timer.setInterval(500)
        timer.timeout.connect(self.dis_update)
        timer.start()

    def dis_update(self):
        """ 타이머 디스플레이 업데이트 """
        real_time = datetime.now().strftime('%Y.%m.%d')
        real_time2 = datetime.now().strftime('%H:%M:%S')
        self.timebarlabel.setText(real_time + " / " + real_time2)


class ReturnBTN(QPushButton):
    qss = """
    QPushButton {
        background: rgb(178, 178, 178);
        border-radius: 6px;
        border: none;
    }
    QPushButton:hover {
        background: rgb(24, 144, 255);
    }
    QPushButton:pressed {
        background: rgb(130, 130, 130);
    }
    """

    def __init__(self, parent):
        super(ReturnBTN, self).__init__()
        self.inmem = make_shmem(parent, self)
        # --------------------------------------------------------------------------------------------------------------
        self.setStyleSheet(self.qss)
        icon = os.path.join(ROOT_PATH, 'img', 'return.png')
        self.setIcon(QIcon(icon))
        self.setIconSize(QSize(60, 60))
        self.setFixedSize(35, 35)
        self.clicked.connect(self.call_return)

    def call_return(self):
        """버튼 명령: 이전 화면 전환"""
        Flag.call_return = True
        # TODO 이전 화면 전화되는 로직 구현 필요


class CloseBTN(QPushButton):
    qss = """
    QPushButton {
        background: rgb(100, 25, 28);
        border-radius: 6px;
        border: none;
    }
    QPushButton:hover {
        background: rgb(184, 25, 28);
    }
    QPushButton:pressed {
        background: rgb(215, 25, 28);
    }
    """

    def __init__(self, parent):
        super(CloseBTN, self).__init__()
        self.inmem = make_shmem(parent, self)
        # --------------------------------------------------------------------------------------------------------------
        self.setStyleSheet(self.qss)
        icon = os.path.join(ROOT_PATH, 'img', 'close.png')
        self.setIcon(QIcon(icon))
        self.setIconSize(QSize(20, 20))
        self.setFixedSize(35, 35)
        self.clicked.connect(self.close)

    def close(self):
        """버튼 명령: 닫기"""
        self.inmem.get_w_id('Mainwindow').close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainTop()
    window.show()
    font = QFontDatabase()
    font.addApplicationFont('./Arial.ttf')
    app.setFont(QFont('Arial'))
    app.exec_()