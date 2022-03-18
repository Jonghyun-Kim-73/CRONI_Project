import os
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import socket

from AIDAA_Ver2.TOOL.TOOL_CNS_UDP_FAST import CNS
from AIDAA_Ver2.TOOL.TOOL_etc import p_, pc_
from AIDAA_Ver2.TOOL.TOOL_Shmem import SHMem, make_shmem
from AIDAA_Ver2.TOOL.TOOL_Widget import ABCWidget, WithNoMargin

from AIDAA_Ver2.Interface import Flag
from AIDAA_Ver2.Interface.main_top import MainTop
from AIDAA_Ver2.Interface.main_0_Lefe import WLMain




from AIDAA_Ver2.Interface.main_top2 import MainTop2

from AIDAA_Ver2.Interface.main_1_left import Main1Left
from AIDAA_Ver2.Interface.main_1_right import Main1Right
from AIDAA_Ver2.Interface.main_2_prog import Main2Prog
from AIDAA_Ver2.Interface.main_3_left import Main3Left
from AIDAA_Ver2.Interface.main_3_right import Main3Right
from AIDAA_Ver2.Interface.main_4_left import Main4Left
from AIDAA_Ver2.Interface.main_4_right import Main4Right

from AIDAA_Ver2.Procedure.ab_procedure import ab_pro
from AIDAA_Ver2.Procedure.symptom_check import symp_check


class Mainwindow(QWidget):
    """메인 윈도우"""
    def __init__(self, shmem, w_widget=None):
        super(Mainwindow, self).__init__()
        self.shmem = shmem
        self.shmem.add_w_id(self)
        self.w_widget = w_widget
        # Main 기본 속성
        self.setGeometry(0, 0, 1920, 1010)
        self.setStyleSheet('background: rgb(128, 128, 128);')
        # 레이아웃 설정
        window_vbox = WithNoMargin(QVBoxLayout(self))
        self.WStack = WithNoMargin(QStackedLayout())        # 하단 섹션
        # 위젯 설정
        self.WTitle = MainTop(self)                         # 타이틀바 위젯
        self.WMain = WMain(self)                            # Main 화면

        # 각 항목을 레이아웃에 배치
        window_vbox.addWidget(self.WTitle)
        window_vbox.addLayout(self.WStack)
        self.WStack.addWidget(self.WMain)

    def closeEvent(self, QCloseEvent):
        pc_(self, 'Close')
        if self.w_widget is not None:
            self.W_myform.closeEvent(QCloseEvent)


class WMain(ABCWidget, QWidget):
    def __init__(self, parent):
        super(WMain, self).__init__(parent)

        window_vobx = WithNoMargin(QVBoxLayout(self), c_m=5)

        WL_Main = WLMain(self)
        window_vobx.addWidget(WL_Main)




    #     main_1_pp.addWidget(Main1Left(self))
    #     main_1_pp.addWidget(Main1Right(self))
    #     main_1 = QWidget(self)
    #     main_1.setLayout(main_1_pp)
    #     self.stack_widget.addWidget(main_1)
    #
    #     # Page 2 (prog-예지)
    #     self.stack_widget.addWidget(Main2Prog(self))
    #
    #     # Page 3 (recv-복구)
    #     main_3_pp = QVBoxLayout()
    #     main_3_pp.setContentsMargins(0, 0, 0, 0)
    #     main_3_pp.setSpacing(0)
    #     main_3_top2 = MainTop2(self)
    #     main_3_pp.addWidget(main_3_top2)
    #     main_3_pp_sub = QHBoxLayout()
    #     main_3_pp_sub.setContentsMargins(0, 0, 0, 0)
    #     main_3_pp_sub.setSpacing(0)
    #     main_3_pp.addLayout(main_3_pp_sub)
    #     main_3_pp_sub.addWidget(Main3Left(self))
    #     # main_3_pp_sub.addWidget(Main3Right(self, 0, 0, 900, 765))
    #     main_3_pp_sub.addWidget(Main3Right(self, 0, 0, 1367, 918))  # 1370, 920
    #     main_3 = QWidget(self)
    #     main_3.setLayout(main_3_pp)
    #     self.stack_widget.addWidget(main_3)
    #
    #     # Page 4 (prss-절차서)
    #     main_4_pp = QVBoxLayout()
    #     main_4_pp.setContentsMargins(0, 0, 0, 0)
    #     main_4_pp.setSpacing(0)
    #     main_4_top2 = MainTop2(self)
    #     main_4_pp.addWidget(main_4_top2)
    #     main_4_pp_sub = QHBoxLayout()
    #     main_4_pp_sub.setContentsMargins(0, 0, 0, 0)
    #     main_4_pp_sub.setSpacing(0)
    #     main_4_pp.addLayout(main_4_pp_sub)
    #     main_4_pp_sub.addWidget(Main4Left(self))
    #     main_4_pp_sub.addWidget(Main4Right(self))
    #     main_4 = QWidget(self)
    #     main_4.setLayout(main_4_pp)
    #     self.stack_widget.addWidget(main_4)
    #

    #
    #     # 테스트
    #     timer1 = QTimer(self)
    #     timer1.setInterval(300)
    #     timer1.timeout.connect(self.call)
    #     timer1.start()
    #
    # def set_frame(self):
    #     """ 메인프레임의 세팅 """
    #     pass
    #
    # def call(self):
    #     """ Flag update """
    #     Flag.main_close = self.close() if Flag.main_close else False
    #
    #     Flag.call_return = self.return_page() if Flag.call_return else False
    #     Flag.call_main = self.change_pp(0) if Flag.call_main else False  # main
    #     Flag.call_prog = self.change_pp(1) if Flag.call_prog else False  # 예지
    #     Flag.call_recv = self.change_pp(2) if Flag.call_recv else False  # 복구
    #     Flag.call_prss = self.change_pp(3) if Flag.call_prss else False  # 절차서
    #     # print(Flag.return_list)
    #     """ SHmem <<-->> Flag """
    #     # TODO 향후 공유 메모리와 Flag의 값 사이의 교환 구현 필요함. ex. AI 계산 결과 -> interface 표현
    #
    #     '''
    #     IF-THEN Rule -> ab_pro
    #     절차서 선택과 상관없이 background에서 모든 절차서의 증상 요건을 확인
    #     제한사항: deque에 데이터가 5초 이상 쌓여 있어야 증감 비교 가능
    #     '''
    #     self.shmem.add_dumy_val()       # IF-THEN 테스트 용 더미 데이터 채우기
    #     symp_check(self.shmem) # IF-THEN 구동
    #     # print(ab_pro['Ab23_06: 증기발생기 전열관 누설']['경보 및 증상'][1]['AutoClick'])
    #
    #     # update
    #     self.update()
    #
    # def change_pp(self, page):
    #     """ page 번호 받아서 stack_widget 페이지로 변경 """
    #     self.stack_widget.setCurrentIndex(page)
    #
    # def return_page(self):
    #     print('Return Page ...')
    #
    #     if len(Flag.return_list) > 1:
    #         Flag.return_list.pop()
    #
    #         if Flag.return_list[-1] == "Main":
    #             Flag.return_page = 0
    #             self.stack_widget.setCurrentIndex(0)
    #             # self.maintop.call_main()
    #         elif Flag.return_list[-1] == "예지":
    #             Flag.return_page = 1
    #             self.stack_widget.setCurrentIndex(1)
    #             # self.maintop.call_prog()
    #     # 뒤로 가면 return list도 하나씩 없애기
    #
    #     # TODO Return page 기능 구현 필요 ...
    #
    # def before_page(self):
    #     print('바로 전 페이지')


if __name__ == '__main__':
    shmem = SHMem(cnsinfo=('1', 100), remoteinfo=('1', 100), max_len_deque=10, test=True,
                  db_path='../DB/db.txt', db_add_path='../DB/db_add.txt')

    app = QApplication(sys.argv)
    app.setStyle("fusion")
    font = QFontDatabase()
    font.addApplicationFont('./Arial.ttf')
    app.setFont(QFont('Arial'))

    w = Mainwindow(shmem)
    w.show()

    sys.exit(app.exec_())