import os
import sys
import pandas as pd
from datetime import datetime

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

ROOT_PATH = os.path.dirname(os.path.abspath(__file__))


class MainRightDiagnosisProgArea(QWidget):
    """ 오른쪽 진단 및 예지 디스플레이 위젯 """
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
        super(MainRightDiagnosisProgArea, self).__init__()
        self.setAttribute(Qt.WA_StyledBackground, True)  # 상위 스타일 상속
        self.parent = parent
        self.setStyleSheet(self.qss)

        self.setMinimumHeight(self.parent.height() - 40)                              # 아래섹션의 기준 크기 <-
        # self.setMaximumWidth(int(self.parent.width()/5) * 2)                          # 1/3 부분을 차지

        # 타이틀 레이어 셋업 ---------------------------------------------------------------------------------------------
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 5, 5, 5)                                         # 왼쪽 여백 고려 x

        label1 = QLabel('Diagnosis area')
        label2 = QLabel('Prognosis area')

        layout.addWidget(label1)
        layout.addWidget(label2)
        self.setLayout(layout)