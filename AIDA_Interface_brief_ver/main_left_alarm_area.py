import os
import sys
import pandas as pd
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
        QPushButton {
            background: rgb(62, 74, 84);
            border-radius: 3px;
            border: 2px inset rgb(62, 74, 84);
            font: bold 12px;
            color: rgb(255, 255, 255);          
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
        layout = QVBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)

        alarm_table_wid = AlarmTable(self)
        # self.alram_reset_btn()

        layout.addWidget(alarm_table_wid)

        # layout1 = QHBoxLayout(self)

        self.Reset = QPushButton('Update')
        self.Reset.clicked.connect(self.test1)
        layout.addWidget(self.Reset)

        self.setLayout(layout)

    def test1(self):
        print('Alarm Update')

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
        col_info = [('경과 시간', 115), ('경보명', 175), ('현재값', 55), ('설정치', 55), ('긴급여부', 0)]

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
        test_action1 = menu.addAction("Add Urgent alarm")
        test_action2 = menu.addAction("Add Normal alarm")

        test_action1.triggered.connect(lambda a, alarm_id=0, urgent=True: self.add_alarm(alarm_id, urgent))
        test_action2.triggered.connect(lambda a, alarm_id=1, urgent=False: self.add_alarm(alarm_id, urgent))
        menu.exec_(event.globalPos())

    def add_alarm(self, alarm_id: int, urgent: bool):
        """ Alarm 1개 추가 기능 """
        row_ = self.rowCount()
        self.insertRow(row_)         # 마지막 Row 에 섹션 추가

        # db load
        db = pd.read_csv('./DB/alarm_info.csv')
        alarm_name_ = db.loc[alarm_id, "alarm_name"]
        criteria = db.loc[alarm_id, "criteria"]
        criteria_id = db.loc[alarm_id, "criteria_id"]

        item_1 = AlarmItemTimer(self)                                         # item 인스턴스 생성
        item_2 = AlarmItemInfo(self, alarm_info = str(alarm_name_))
        item_3 = AlarmItemInfo(self, alarm_info = str(criteria))
        item_4 = AlarmItemInfo(self, '0')
        item_5 = AlarmItemCondition(self, alarm_info = str(alarm_name_),
                                    urgent=urgent, blink=True)                # item 인스턴스 생성

        self.setCellWidget(row_, 0, item_1)
        self.setCellWidget(row_, 1, item_2)
        self.setCellWidget(row_, 2, item_3)
        self.setCellWidget(row_, 3, item_4)
        self.setCellWidget(row_, 4, item_5)
        pass

class AlarmButton(QPushButton):
    """알람 history 및 reset 버튼"""
    qss = """
        QPushbutton#History {
            background: rgb(213, 213, 213);          
        }
         QPushbutton#AlarmButton {
            background: rgb(246, 246, 246);         
        }  
    """


class AlarmItemInfo(QLabel):
    """ 긴급 여부 판단 아이템 """
    qss = """
        QLabel#AlarmItemInfo {
            background: rgb(62, 72, 84);
            border-radius: 3px;
            font-size: 11px;
            color: rgb(255, 255, 255);
        }

        QLabel#AlarmItemInfo:hover {
            background: rgb(255, 193, 7);
            color: rgb(31, 39, 42);
        }

        QLabel#AlarmItemInfo:selected {
            background: rgb(255, 193, 7);
            color: rgb(31, 39, 42);
        }
    """

    def __init__(self, parent, alarm_info):
        super(AlarmItemInfo, self).__init__()
        self.setAttribute(Qt.WA_StyledBackground, True)  # 상위 스타일 상속
        self.parent = parent

        self.setStyleSheet(self.qss)
        self.setObjectName('AlarmItemInfo')

        self.dis_update(alarm_info)

    def dis_update(self, alarm_name):
        """ 알람 정보 디스플레이 업데이트 """
        self.setText(alarm_name)
        self.setAlignment(Qt.AlignVCenter | Qt.AlignCenter)  # 텍스트 정렬


class AlarmItemTimer(QLabel):
    """ 발생 시간 타이머 아이템 """
    qss = """
            QLabel#AlarmItemTimer {
                background: rgb(62, 72, 84);
                border-radius: 3px;
                font-size: 11px;
                color: rgb(255, 255, 255);
            }

            QLabel#AlarmItemTimer:hover {
                background: rgb(255, 193, 7);
                color: rgb(31, 39, 42);
            }

            QLabel#AlarmItemTimer:selected {
                background: rgb(255, 193, 7);
                color: rgb(31, 39, 42);
            }
    """

    def __init__(self, parent):
        super(AlarmItemTimer, self).__init__()
        self.setAttribute(Qt.WA_StyledBackground, True)  # 상위 스타일 상속
        self.parent = parent

        self.setStyleSheet(self.qss)
        self.setObjectName('AlarmItemTimer')

        self.dis_update()

    def dis_update(self, load_realtime=True):
        """ 타이머 디스플레이 업데이트 """
        if load_realtime:
            real_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        else:
            # TODO 나중에 CNS 변수 사용시 real_time 부분 수정할 것.
            real_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.setText(real_time)
        self.setAlignment(Qt.AlignVCenter | Qt.AlignCenter)  # 텍스트 정렬


class AlarmItemCondition(QLabel):
    """ 긴급 여부 판단 아이템 """
    qss = """
        QLabel#AlarmItemCondition {
            background: rgb(62, 72, 84);
            border-radius: 3px;
            color: rgb(255, 255, 255);
        }
        
        QLabel#AlarmItemCondition:hover {
            background: rgb(255, 193, 7);
            color: rgb(31, 39, 42);
        }
        
        QLabel#AlarmItemCondition:selected {
            background: rgb(255, 193, 7);
            color: rgb(31, 39, 42);
        }
        
        QLabel#AlarmItemCondition[Blink=true][Urgent=true] {
            background: rgb(248, 108, 107);
        }
        QLabel#AlarmItemCondition[Blink=true][Urgent=false] {
            background: rgb(255, 193, 7);
        }
        QLabel#AlarmItemCondition[Blink=false] {
            background: rgb(62, 72, 84);
        }
    """

    def __init__(self, parent, alarm_info, urgent=False, blink=False, blink_time=500):
        super(AlarmItemCondition, self).__init__()
        self.setAttribute(Qt.WA_StyledBackground, True)  # 상위 스타일 상속
        self.parent = parent
        self.procedure_area = self.parent.parent.parent.procedure_area

        self.setStyleSheet(self.qss)
        self.setObjectName('AlarmItemCondition')

        # procedure area 로 넘겨서 알람의 정보에 대한 절차서 찾을수 있는 힌트 제공
        self.alarm_info = alarm_info
        self.setProperty("Urgent", urgent)
        if blink:
            self.setProperty("Blink", True)
            # timer section
            timer = QTimer(self)
            timer.setInterval(blink_time)
            timer.timeout.connect(self.dis_update)
            timer.start()

    def dis_update(self):
        if self.property("Blink"):
            self.setProperty("Blink", False)
        else:
            self.setProperty("Blink", True)
        self.setStyleSheet(self.qss)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            if self.procedure_area.fold_cond is False:
                """ 경보 절차서 디스플레이가 접힌 상태로 클릭시 펼쳐짐 """
                # procedure area 로 넘겨서 알람의 정보에 대한 절차서 찾을수 있는 힌트 제공
                self.procedure_area.run_fold(self, True, self.alarm_info)
            else:
                """ 경보 절차서가 펼쳐진 상태에 동일 알람 눌러야 꺼짐 아니면 내용만 업데이트"""
                if self == self.procedure_area.who_clicked:
                    self.procedure_area.run_fold(self, False, self.alarm_info)
                else:
                    self.procedure_area.run_update_info(self, self.alarm_info)

