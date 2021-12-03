import os
import sys
from datetime import datetime

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from AIDAA_Ver2.Interface import Flag

ROOT_PATH = os.path.dirname(os.path.abspath(__file__))


class MainTop(QWidget):
    qss = """
        QWidget {
            background: rgb(128, 128, 128);
            border: 0px solid rgb(0, 0, 0);
            border-radius: 6px;
        }
        QPushButton#main1{
            background: rgb(0, 176, 218);
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
    # qss = """
    #     QWidget {
    #         background: rgb(128, 128, 128);
    #         border: 0px solid rgb(0, 0, 0);
    #         border-radius: 6px;
    #     }
    #     QWidget#ChangePP[Condition="Hover"] {
    #         background: rgb(24, 144, 255);                  /* 호버 임시 낮은 % 색상 */
    #     }
    #     QWidget#ChangePP[Condition="Click"] {
    #         background: rgb(24, 144, 255);                    /* 활성화 o */
    #     }
    #     QWidget#ChangePP[Condition="Non-Click"] {
    #         background: rgb(231, 231, 234);                 /* 활성화 x */
    #     }
    #     QPushButton{
    #         border-radius: 6px;
    #     }
    #     """


    def __init__(self):
        super(MainTop, self).__init__()

        self.bar_height = 35
        self.setStyleSheet(self.qss)

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
        label1.clicked.connect(self.call_main)

        #AlignVCenter 수직가운데정렬 / AlignHCenter 수평가운데정렬 / AlignCenter 모두 적용
        # label1.setAlignment(Qt.AlignCenter)
        label1.setFixedHeight(self.bar_height)
        label1.setFixedWidth(620)

        label2 = QPushButton("예지")
        label2.setObjectName('main2')
        label2.clicked.connect(self.call_prog)

        # label2.setAlignment(Qt.AlignCenter)
        label2.setFixedHeight(self.bar_height)
        label2.setFixedWidth(620)

        btn_return = ReturnBTN()
        btn_close = CloseBTN()

        layout.addWidget(widget1)
        layout.addWidget(label0)
        layout.addWidget(label1)
        layout.addWidget(label2)
        layout.addWidget(btn_return)
        layout.addWidget(btn_close)

    def call_main(self):
        Flag.call_main = True

    def call_prog(self):
        Flag.call_prog = True


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
        timer.setInterval(500)
        timer.timeout.connect(self.dis_update)
        timer.start()

    def dis_update(self):
        """ 타이머 디스플레이 업데이트 """
        real_time = datetime.now().strftime('%Y.%m.%d')
        real_time2 = datetime.now().strftime('%H:%M:%S')
        self.timebarlabel.setText(real_time + " / " + real_time2)

# dis_updata의 1초간격으로 하위 항목들이 업데이트 됨
    # 라벨들을 얹어놓고 라벨들의 상태에 따라 업데이트가 되도록 해야함
    # 라벨1: Main / 라벨2: 예지
    # Click 상태_ / Non_Click 상태_/ Hover 상태
    # Default_ 라벨1 Click / 라벨2 Non_Click


    # def click_status(self, name):
    #     for i, n in enumerate(self.name_list):
    #         if n == name:
    #             # print(f'{n} is clicked.')
    #             self.btn_[n].update_info('Click')
    #             self.main_stack_widget.setCurrentIndex(i)
    #         else:
    #             self.btn_[n].update_info('Non-Click')
    #
    # def update_info(self, condition):
    #     self.setProperty("Condition", condition)
    #     self.style().polish(self)
    #     if not condition == 'Hover':
    #         self._cond = condition
    #
    # def paintEvent(self, a0: QPaintEvent) -> None:
    #     print('test')

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

    def __init__(self):
        super(ReturnBTN, self).__init__()
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

    def __init__(self):
        super(CloseBTN, self).__init__()
        self.setStyleSheet(self.qss)
        icon = os.path.join(ROOT_PATH, 'img', 'close.png')
        self.setIcon(QIcon(icon))
        self.setIconSize(QSize(20, 20))
        self.setFixedSize(35, 35)
        self.clicked.connect(self.close)

    def close(self):
        """버튼 명령: 닫기"""
        Flag.main_close = True


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainTop()
    window.show()
    font = QFontDatabase()
    font.addApplicationFont('./Arial.ttf')
    app.setFont(QFont('Arial'))
    app.exec_()