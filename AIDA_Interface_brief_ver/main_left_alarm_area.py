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
    def __init__(self, parent=None, mem=None):
        super(MainLeftAlarmArea, self).__init__(parent=parent)
        self.mem = mem
        self.setAttribute(Qt.WA_StyledBackground, True)  # 상위 스타일 상속
        self.setObjectName('SubW')
        self.setMaximumWidth(int(self.parentWidget().width()/5) * 3)                          # 1/3 부분을 차지

        # 타이틀 레이어 셋업 ---------------------------------------------------------------------------------------------
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # 1. 알람 Table
        alarm_label = QLabel('경보 Area')
        alarm_label.setMinimumHeight(30)
        alarm_table_wid = ArarmArea(self, self.mem)
        # 2. 알람 Table btn
        alarm_tabel_btn = AlarmSuppressionButton(self)  # 'Suppression Btn')
        # 3. 예지 Area
        prog_label = QLabel('예지 Area')
        prog_label.setMinimumHeight(30)
        prog_area = ProgArea(self)

        # --------------------------------------------------------------------------------------------------------------
        layout.addWidget(alarm_label)
        layout.addWidget(alarm_table_wid)
        layout.addSpacing(5)
        layout.addWidget(alarm_tabel_btn)
        layout.addSpacing(10)
        layout.addWidget(prog_label)
        layout.addWidget(prog_area)

        self.setLayout(layout)

    def test1(self):
        print('Alarm Update')

# ----------------------------------------------------------------------------------------------------------------------


class ArarmArea(QWidget):
    def __init__(self, parent, mem=None):
        super(ArarmArea, self).__init__(parent=parent)
        self.mem = mem
        self.setAttribute(Qt.WA_StyledBackground, True)  # 상위 스타일 상속
        self.setObjectName('SubArea')

        # 타이틀 레이어 셋업 ---------------------------------------------------------------------------------------------
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.alarm_table = AlarmTable(self, self.mem)
        # --------------------------------------------------------------------------------------------------------------

        layout.addWidget(self.alarm_table)
        self.setLayout(layout)


class AlarmTable(QTableWidget):
    """ 알람 테이블 위젯 """
    def __init__(self, parent, mem):
        super(AlarmTable, self).__init__(parent=parent)
        self.mem = mem
        self.setAttribute(Qt.WA_StyledBackground, True)  # 상위 스타일 상속
        self.setObjectName('AlarmTable')

        # 테이블 프레임 모양 정의
        self.verticalHeader().setVisible(False)     # Row 넘버 숨기기

        # 테이블 셋업
        col_info = [('긴급여부', 60), ('경보명', 250), ('현재값', 55), ('설정치', 55), ('발생시간', 0)]

        self.setColumnCount(len(col_info))

        col_names = []
        for i, (l, w) in enumerate(col_info):
            self.setColumnWidth(i, w)
            col_names.append(l)

        self.max_cell = 10

        for i in range(0, self.max_cell):
            self.add_empty_alarm(i)

        cell_height = self.rowHeight(0)
        total_height = self.horizontalHeader().height() + cell_height * self.max_cell + 4        # TODO 4 매번 계산.

        self.parent().setMaximumHeight(total_height)
        self.setMaximumHeight(total_height)

        self.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.verticalScrollBar().setSingleStep(cell_height/3)

        self.setHorizontalHeaderLabels(col_names)
        self.horizontalHeader().setStretchLastSection(True)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)

        self.emergec_alarm_dict = {

        }

        if self.mem != None:
            # timer section
            timer = QTimer(self)
            timer.setInterval(1000)
            timer.timeout.connect(self._update_mem_to_alarm_panel)
            timer.start()

    def _update_mem_to_alarm_panel(self):
        self.local_mem = self.mem.get_shmem_db()
        print(self.local_mem['KLAMPO271']['Val'], self.local_mem['ZVCT']['Val'])

        if self._check_alarm_cond('KLAMPO251'):
            self.emergec_alarm_dict['KLAMPO251'] = 'On'
            self._add_alarm('KLAMPO251', self.local_mem['XPIRM']['Val'], self.local_mem['CIRFH']['Val'], False)

        if self._check_alarm_cond('KLAMPO271'):
            self.emergec_alarm_dict['KLAMPO271'] = 'On'
            self._add_alarm('KLAMPO271', self.local_mem['ZVCT']['Val'], self.local_mem['CZVCT6']['Val'], False)

    def _check_alarm_cond(self, para):
        if self.local_mem[para]['Val'] == 1:
            if not para in self.emergec_alarm_dict.keys():
                return True
            else:
                return False
        else:
            return False

    def contextMenuEvent(self, event) -> None:
        """ AlarmTable 기능 테스트 """
        menu = QMenu(self)
        test_action1 = menu.addAction("Add Urgent alarm")
        test_action2 = menu.addAction("Add Normal alarm")

        test_action1.triggered.connect(lambda a, alarm_id=0, urgent=True: self.add_alarm(alarm_id, urgent))
        test_action2.triggered.connect(lambda a, alarm_id=1, urgent=False: self.add_alarm(alarm_id, urgent))
        menu.exec_(event.globalPos())

    def add_empty_alarm(self, i):
        self.insertRow(i)
        [self.setCellWidget(i, _, AlarmEmptyCell(self)) for _ in range(0, 5)]

    def add_alarm(self, alarm_id: int, urgent: bool):
        """ Alarm 1개 추가 기능 """
        # db load
        db = pd.read_csv('./DB/alarm_info.csv')
        alarm_name_ = db.loc[alarm_id, "alarm_name"]
        criteria = db.loc[alarm_id, "criteria"]
        criteria_id = db.loc[alarm_id, "criteria_id"]
        self._add_alarm(alarm_name_, 0, criteria, urgent)

    def _add_alarm(self, alarm_name_, currnet, criteria, urgent):
        item_1 = AlarmItemInfo(self, alarm_info='R' if urgent else 'N')
        item_2 = AlarmItemInfo(self, alarm_info=str(alarm_name_))
        item_3 = AlarmItemInfo(self, alarm_info=str(currnet))
        item_4 = AlarmItemInfo(self, alarm_info=str(criteria))
        item_5 = AlarmItemTimer(self)                                           # item 인스턴스 생성

        # 비어 있지 않은 셀 탐색 후 아래에서 위로 데이터 쌓기
        add_row_pos = 0
        for _ in range(0, self.rowCount()):
            if self.cellWidget(_, 0).isempty:
                add_row_pos += 1

        self.insertRow(add_row_pos)  # 마지막 Row 에 섹션 추가

        self.setCellWidget(add_row_pos, 0, item_1)
        self.setCellWidget(add_row_pos, 1, item_2)
        self.setCellWidget(add_row_pos, 2, item_3)
        self.setCellWidget(add_row_pos, 3, item_4)
        self.setCellWidget(add_row_pos, 4, item_5)

        if self.cellWidget(0, 0).isempty:
            # 비어있는 경우 맨 윗줄 지우기
            self.removeRow(0)
        else:
            pass
        self.scrollToTop()
        pass


class AlarmSuppressionButton(QPushButton):
    """알람 Suppression 버튼"""
    def __init__(self, parent):
        super(AlarmSuppressionButton, self).__init__(parent=parent)
        self.setAttribute(Qt.WA_StyledBackground, True)  # 상위 스타일 상속
        self.setObjectName('Btn')

        self.setText('Suppression Btn')

        self.clicked.connect(self._run)

    def _run(self):
        # TODO Suppresion 버튼 기능 추가.
        print(self, 'Suppression Btn clicked')


class AlarmEmptyCell(QLabel):
    """ 공백 Cell """
    def __init__(self, parent):
        super(AlarmEmptyCell, self).__init__(parent=parent)
        self.setAttribute(Qt.WA_StyledBackground, True) # 상위 스타일 상속
        self.setObjectName('AlarmItemEmpty')
        self.isempty = True


class AlarmItemInfo(QLabel):
    """ 긴급 여부 판단 아이템 """
    def __init__(self, parent, alarm_info):
        super(AlarmItemInfo, self).__init__(parent=parent)
        self.setAttribute(Qt.WA_StyledBackground, True)  # 상위 스타일 상속
        self.setObjectName('AlarmItemInfo')
        self.isempty = False
        self.dis_update(alarm_info)

    def dis_update(self, alarm_name):
        """ 알람 정보 디스플레이 업데이트 """
        self.setText(alarm_name)
        self.setAlignment(Qt.AlignVCenter | Qt.AlignCenter)  # 텍스트 정렬


class AlarmItemTimer(QLabel):
    """ 발생 시간 타이머 아이템 """
    def __init__(self, parent):
        super(AlarmItemTimer, self).__init__(parent=parent)
        self.setAttribute(Qt.WA_StyledBackground, True)  # 상위 스타일 상속
        self.setObjectName('AlarmItemInfo')
        self.isempty = False
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


# ----------------------------------------------------------------------------------------------------------------------

class ProgArea(QWidget):
    def __init__(self, parent):
        super(ProgArea, self).__init__(parent=parent)
        self.setAttribute(Qt.WA_StyledBackground, True)  # 상위 스타일 상속
        self.setObjectName('SubArea')

        # 타이틀 레이어 셋업 ---------------------------------------------------------------------------------------------
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(0)

        label1 = QLabel('Trip 예정 시간')

        label2 = QLabel('Trip 예상 기여 변수')

        # --------------------------------------------------------------------------------------------------------------
        layout.addWidget(label1)
        layout.addSpacing(50)
        layout.addWidget(label2)
        layout.addSpacing(120)

        self.setLayout(layout)



