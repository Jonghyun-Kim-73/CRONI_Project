import os
import sys
from datetime import datetime

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

ROOT_PATH = os.path.dirname(os.path.abspath(__file__))


class MainLeftAlarmArea(QWidget):
    """ 왼쪽 알람 디스플레이 위젯 """
    qss = """
        QWidget {
            background: rgb(14, 22, 24);
        }
    """

    def __init__(self, parent=None):
        super(MainLeftAlarmArea, self).__init__()
        self.setAttribute(Qt.WA_StyledBackground, True)  # 상위 스타일 상속
        self.parent = parent
        self.setStyleSheet(self.qss)

        self.setMinimumHeight(self.parent.height() - 40)                              # 아래섹션의 기준 크기 <-
        self.setMaximumWidth(int(self.parent.width()/5) * 2)                          # 1/3 부분을 차지

        # 타이틀 레이어 셋업 ---------------------------------------------------------------------------------------------
        layout = QHBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)

        alarm_table_wid = AlarmTable(self)

        layout.addWidget(alarm_table_wid)
        self.setLayout(layout)

class AlarmTable(QTableWidget):
    """ 알람 테이블 위젯 """
    qss = """
        QTableWidget#AlarmTable {
            background: rgb(31, 39, 42);
            border-radius: 6px;
            border: none;
        }
        
        QTableWidget#AlarmTable QHeaderView::section {
            background: rgb(31, 39, 42);
            border-radius: 3px;
            border: 2px inset rgb(62, 74, 84);
            font: bold 12px;
            color: rgb(255, 255, 255);
        }
        
        QTableWidget#AlarmTable::item {
            background: rgb(62, 72, 84);
            border-radius: 3px;
            color: rgb(255, 255, 255);
        }
        
        QTableWidget#AlarmTable::item:hover {
            background: rgb(213, 149, 88);
            color: rgb(31, 39, 42);
        }
        
        QTableWidget#AlarmTable::item:selected {
            background: rgb(213, 149, 88);
            color: rgb(31, 39, 42);
        }
    """
    def __init__(self, parent):
        super(AlarmTable, self).__init__()
        self.setAttribute(Qt.WA_StyledBackground, True)  # 상위 스타일 상속
        self.parent = parent

        self.setStyleSheet(self.qss)
        self.setObjectName('AlarmTable')

        self.setFixedWidth(self.parent.width() - 10)
        self.setFixedHeight(self.parent.height() - 10)

        # 테이블 프레임 모양 정의
        self.verticalHeader().setVisible(False)     # Row 넘버 숨기기

        # 테이블 셋업
        col_info = [('경과 시간', 90), ('경보명', 180), ('현재값', 70), ('설정치', 70), ('긴급여부', 0)]

        self.setColumnCount(len(col_info))

        col_names = []
        for i, (l, w) in enumerate(col_info):
            self.setColumnWidth(i, w)
            col_names.append(l)

        self.setHorizontalHeaderLabels(col_names)
        self.horizontalHeader().setStretchLastSection(True)

    def contextMenuEvent(self, event) -> None:
        """ AlarmTable 기능 테스트 """
        menu = QMenu(self)
        test_action1 = menu.addAction("Add alarm")

        test_action1.triggered.connect(lambda a, info='info': self.add_alarm(info))
        menu.exec_(event.globalPos())

    def add_alarm(self, info: str):
        """ Alarm 1개 추가 기능 """
        self.insertRow(self.rowCount())         # 마지막 Row 에 섹션 추가
        pass
