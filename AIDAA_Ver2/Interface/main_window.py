import os
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from AIDAA_Ver2.TOOL.TOOL_etc import p_
from AIDAA_Ver2.TOOL.TOOL_Shmem import SHMem

from AIDAA_Ver2.Interface import Flag
from AIDAA_Ver2.Interface.main_top import MainTop
from AIDAA_Ver2.Interface.main_top2 import MainTop2

from AIDAA_Ver2.Interface.main_1_left import Main1Left
from AIDAA_Ver2.Interface.main_1_right import Main1Right
from AIDAA_Ver2.Interface.main_2_prog import Main2Prog
from AIDAA_Ver2.Interface.main_3_left import Main3Left
from AIDAA_Ver2.Interface.main_3_right import Main3Right
from AIDAA_Ver2.Interface.main_4_left import Main4Left
from AIDAA_Ver2.Interface.main_4_right import Main4Right

import time


class Mainwindow(QWidget):
    """메인 윈도우"""
    qss = """
    QWidget {background: rgb(128, 128, 128);}
    """

    def __init__(self, parent):
        super(Mainwindow, self).__init__()
        self.shmem = parent.shmem   # <- myform.shmem
        self.W_myform = parent

        # Main 기본 속성
        self.setGeometry(0, 0, 1920, 1010)
        self.setStyleSheet(self.qss)

        # 레이아웃 설정
        window_vbox = QVBoxLayout()  # 세로 방향 레이아웃
        window_vbox.setContentsMargins(0, 0, 0, 0)  # 여백
        window_vbox.setSpacing(0)  # 각 객체 사이의 여백

        # 타이틀바 위젯
        self.BB = MainTop()

        # 하단 섹션
        self.stack_widget = QStackedLayout()
        self.stack_widget.setContentsMargins(0, 0, 0, 0)
        self.stack_widget.setSpacing(0)

        # Page 1 (main-초기 main)
        main_1_pp = QHBoxLayout(self)
        main_1_pp.setContentsMargins(0, 0, 0, 0)
        main_1_pp.setSpacing(0)
        main_1_pp.addWidget(Main1Left(self))
        main_1_pp.addWidget(Main1Right(self))
        main_1 = QWidget(self)
        main_1.setLayout(main_1_pp)
        self.stack_widget.addWidget(main_1)

        # Page 2 (prog-예지)
        self.stack_widget.addWidget(Main2Prog(self))

        # Page 3 (recv-복구)
        main_3_pp = QVBoxLayout()
        main_3_pp.setContentsMargins(0, 0, 0, 0)
        main_3_pp.setSpacing(0)
        main_3_top2 = MainTop2(self)
        main_3_pp.addWidget(main_3_top2)
        main_3_pp_sub = QHBoxLayout()
        main_3_pp_sub.setContentsMargins(0, 0, 0, 0)
        main_3_pp_sub.setSpacing(0)
        main_3_pp.addLayout(main_3_pp_sub)
        main_3_pp_sub.addWidget(Main3Left(self))
        # main_3_pp_sub.addWidget(Main3Right(self, 0, 0, 900, 765))
        main_3_pp_sub.addWidget(Main3Right(self, 0, 0, 1367, 918))  # 1370, 920
        main_3 = QWidget(self)
        main_3.setLayout(main_3_pp)
        self.stack_widget.addWidget(main_3)

        # Page 4 (prss-절차서)
        main_4_pp = QVBoxLayout()
        main_4_pp.setContentsMargins(0, 0, 0, 0)
        main_4_pp.setSpacing(0)
        main_4_top2 = MainTop2(self)
        main_4_pp.addWidget(main_4_top2)
        main_4_pp_sub = QHBoxLayout()
        main_4_pp_sub.setContentsMargins(0, 0, 0, 0)
        main_4_pp_sub.setSpacing(0)
        main_4_pp.addLayout(main_4_pp_sub)
        main_4_pp_sub.addWidget(Main4Left(self))
        main_4_pp_sub.addWidget(Main4Right(self))
        main_4 = QWidget(self)
        main_4.setLayout(main_4_pp)
        self.stack_widget.addWidget(main_4)

        # 각 항목을 레이아웃에 배치
        window_vbox.addWidget(self.BB)
        window_vbox.addLayout(self.stack_widget)
        #
        self.setLayout(window_vbox)
        # self.showMaximized() <- 초기 Geometry 의 크기에 따라감. 삭제.

    def set_frame(self):
        """ 메인프레임의 세팅 """
        pass

    def paintEvent(self, e):
        """ Flag update """
        Flag.main_close = self.close() if Flag.main_close else False
        Flag.call_return = self.return_page() if Flag.call_return else False
        Flag.call_main = self.change_pp(0) if Flag.call_main else False
        Flag.call_prog = self.change_pp(1) if Flag.call_prog else False
        Flag.call_recv = self.change_pp(2) if Flag.call_recv else False
        Flag.call_prss = self.change_pp(3) if Flag.call_prss else False

        """ SHmem <<-->> Flag """
        # TODO 향후 공유 메모리와 Flag의 값 사이의 교환 구현 필요함. ex. AI 계산 결과 -> interface 표현

    def change_pp(self, page):
        """ page 번호 받아서 stack_widget 페이지로 변경 """
        self.stack_widget.setCurrentIndex(page)

    def return_page(self):
        print('Return Page ...')
        # TODO Return page 기능 구현 필요 ...

    def closeEvent(self, QCloseEvent):
        p_(__file__, 'Close')
        self.W_myform.closeEvent(QCloseEvent)


class DumyWindow(QWidget):
    def __init__(self, shmem):
        super(DumyWindow, self).__init__()
        self.shmem = shmem

        self.setGeometry(0, 0, 100, 100)

        self.cns_main_win = Mainwindow(self)
        self.cns_main_win.show()

    def closeEvent(self, QCloseEvent):
        p_(__file__, 'Close')
        sys.exit()


if __name__ == '__main__':
    """ Interface 개발자 TEST 용 """
    # 1. 더미 Shared Mem
    shmem = SHMem(cnsinfo=('192.0.0.1', 7000), remoteinfo=('192.0.0.1', 7000), max_len_deque=2,
                  db_path='../DB/db.txt', db_add_path='../DB/db_add.txt')

    # 2. Call Interface
    app = QApplication(sys.argv)
    app.setStyle("fusion")

    window = DumyWindow(shmem)
    window.show()

    font = QFontDatabase()
    font.addApplicationFont('./Arial.ttf')
    app.setFont(QFont('Arial'))
    app.exec_()