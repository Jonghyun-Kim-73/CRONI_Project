import os
import sys
import pandas as pd
from datetime import datetime

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

ROOT_PATH = os.path.dirname(os.path.abspath(__file__))


class MainCenterProcedureArea(QWidget):
    """ 가운데 경보 절차서 디스플레이 위젯 """
    qss = """
        QWidget {
            background: rgb(14, 22, 24);
        }
        QLabel {
            background: rgb(31, 39, 42);
            border-radius: 6px;
            color: rgb(255, 255, 255);
        }
    """

    def __init__(self, parent=None):
        super(MainCenterProcedureArea, self).__init__()
        self.setAttribute(Qt.WA_StyledBackground, True)  # 상위 스타일 상속
        self.parent = parent
        self.setStyleSheet(self.qss)

        self.setMinimumHeight(self.parent.height() - 40)                              # 아래섹션의 기준 크기 <-
        # self.setMaximumWidth(int(self.parent.width()/5) * 2)                          # 1/3 부분을 차지

        # 타이틀 레이어 셋업 ---------------------------------------------------------------------------------------------
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 5, 5, 5)                                         # 왼쪽 여백 고려 x

        """
        main_left_alarm_arae 의 하위 AlarmItemCondition 을 클릭하면 옆의 정보 받아서 업데이트됨.
        """
        self.label1 = QLabel('-')

        layout.addWidget(self.label1)
        self.setLayout(layout)

        #
        self.fold_cond = False
        self.who_clicked = None
        self.setMaximumWidth(0)

        self.fold_time = 200
        self.fold_max_pos, self.fold_min_pos = 200, 0

        self.ani = QPropertyAnimation(self, b'maximumWidth')
        self.ani.setDuration(self.fold_time)

    def run_update_info(self, who, info):
        self.who_clicked = who
        self.label1.setText(info)
        self.fold_cond = True

    def run_fold(self, who, fold, info):
        self.who_clicked = who
        if fold:
            self.label1.setText(info)
            self.ani.setStartValue(self.fold_min_pos)
            self.ani.setEndValue(self.fold_max_pos)
            self.ani.start()
            self.fold_cond = True
        else:
            self.ani.setStartValue(self.fold_max_pos)
            self.ani.setEndValue(self.fold_min_pos)
            self.ani.start()
            self.fold_cond = False
