import os
import sys

import numpy
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import socket
from collections import deque
from datetime import datetime

from AIDAA_Ver2.TOOL.TOOL_Shmem import SHMem
from AIDAA_Ver2.TOOL.TOOL_Widget import *
from AIDAA_Ver2.Interface.main_0_Left_Pop import Popup


class WLMain(ABCWidget):
    qss = """
            QWidget {
                background: rgb(231, 231, 234);
                border: 0px solid rgb(0, 0, 0); 
                font-size: 14pt;
            }
            QPushButton{
                background: White;
                color: Black;
            }
            QHeaderView::section {
                background: rgb(128, 128, 128);
                font-size:14pt;
                border:0px solid;
            }
            QHeaderView {
                border:1px solid rgb(128, 128, 128);
            }
            QTableView::item {
                padding:50px;
                font-size:14pt;
            }
        """

    def __init__(self, parent):
        super(WLMain, self).__init__(parent)
        self.setStyleSheet(self.qss)
        layout = WithNoMargin(QVBoxLayout(self), c_m=5)
        layout.addWidget(WAlarmTable(parent=self, hcell=30, ncell=30))     # hcell 는 3의 배수
        layout.addWidget(SuppressBTN('Suppress button', self))


class SuppressBTN(ABCPushButton):
    def __init__(self, str, parent):
        super(SuppressBTN, self).__init__(parent, str)
        self.setFixedHeight(30)
        self.clicked.connect(self.call_Suppress)

    def call_Suppress(self):
        self.inmem.get_w_id('WAlarmTableModel').remove_mismatch_alarm()


class WAlarmTable(ABCTableView, QTableView):
    def __init__(self, **kwargs):
        super(WAlarmTable, self).__init__(**kwargs)
        self.setModel(WAlarmTableModel(self))
        self.set_body()
        self.set_horizontal()
        self.set_vertical()
        self.doubleClicked.connect(self.call_double_click)

    def set_horizontal(self):
        self.horizontalHeader().setDefaultAlignment(Qt.AlignmentFlag.AlignCenter)
        self.horizontalHeader().setFixedHeight(self.hcell)
        self.horizontalHeader().setDefaultSectionSize(self.hcell)
        self.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        [self.setColumnWidth(i+1, s) for i, s in enumerate([150, 150, 100, 80, 100])]
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

    def set_vertical(self):
        self.verticalHeader().hide()
        self.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Fixed)
        self.verticalHeader().setDefaultSectionSize(self.hcell)
        self.setVerticalScrollMode(QAbstractItemView.ScrollMode.ScrollPerPixel)
        self.verticalScrollBar().setSingleStep(self.hcell/3)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)

    def set_body(self):
        self.setShowGrid(False)
        self.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.setSelectionBehavior(QTableWidget.SelectRows)
        self.setFixedHeight(self.hcell * (self.ncell + 1))

    def paintEvent(self, e: QPaintEvent) -> None:
        super(WAlarmTable, self).paintEvent(e)
        qp = QPainter(self.viewport())
        qp.save()
        self.draw_row_line(qp)
        #self.draw_col_line(qp)
        qp.restore()

    def call_double_click(self, index):
        alarm_des = self.inmem.shmem.get_alarm_des(self.inmem.get_w_id('WAlarmTableModel').get_row_alarm_name(index))
        if alarm_des != '':
            self.popup = Popup(file_path=os.path.abspath(os.path.join(os.path.dirname(__file__), "test.pdf")),
                               alarm_des=alarm_des)
            self.popup.show()


class WAlarmTableModel(ABCAbstractTableModel, QAbstractTableModel):
    column_label = ['DESCRIPTION', 'VALUE', 'SETPOINT', 'UNIT', 'DATE', 'TIME']
    num_alarm = 0

    def __init__(self, parent):
        super(WAlarmTableModel, self).__init__(parent)
        self.dis_alarm = {'alarm': {'Time': '00:00:00'}}
        self.dis_data = deque([])
        self.alarm_cnt = None
        self.blick = False
        fun_updater(self, 500, [self.update_table])

    def update_table(self):
        # TEST 로직
        if self.num_alarm == 2:
            self.inmem.shmem.change_shmem_val('UCCWIN', 1)
            self.inmem.shmem.change_shmem_db(self.inmem.shmem.get_shmem_db())
        if self.num_alarm == 5:
            self.inmem.shmem.change_shmem_val('UCCWIN', -1)
            self.inmem.shmem.change_shmem_db(self.inmem.shmem.get_shmem_db())
        if self.num_alarm == 20:
            self.inmem.shmem.change_shmem_val('UCCWIN', 1)
            self.inmem.shmem.change_shmem_db(self.inmem.shmem.get_shmem_db())
        self.num_alarm += 1
        # -----------------------------------------------------------
        self.alarm_cnt = self.inmem.shmem.get_occur_alarm_info()
        [self.add_new_alarm(alarm) for alarm in self.alarm_cnt.keys()]      # 새롭게 발생한 알람 추가

        # layout 업데이트
        self.layoutAboutToBeChanged.emit()
        self.layoutChanged.emit()

        self.blick = False if self.blick else True

    def add_new_alarm(self, occ_alarm):
        if not occ_alarm in self.dis_alarm.keys():
            self.dis_alarm[occ_alarm] = {'Time': datetime.now()}
            # 앞쪽에 넣기
            self.dis_data.appendleft([self.alarm_cnt[occ_alarm], 0.5, 0.2, "kg/cm",
                                      datetime.now().strftime('%m.%d'),
                                      datetime.now().strftime('%H:%M:%S'),
                                      occ_alarm,
                                      ])

    def find_idx(self, alarm_name):
        """ dis_data 에서 해당 알람 이름을 가진 list 의 위치 반환 """
        for idx, data  in enumerate(self.dis_data):
            if data[-1] == alarm_name:
                return idx
        return None

    def find_mismatch_list(self):
        """ display 된 알람 중에서 현재 만족 상태 (꺼진 알람) 인 알람 변수 추출 """
        alarm_names = []
        if not self.alarm_cnt is None:
            for d_alarm in self.dis_alarm.keys():
                if d_alarm not in self.alarm_cnt.keys():
                    alarm_names.append(d_alarm)
        return alarm_names

    def remove_mismatch_alarm(self):
        while True:
            if len(self.find_mismatch_list()) != 1:
                del self.dis_data[self.find_idx(self.find_mismatch_list()[1])]
                del self.dis_alarm[self.find_mismatch_list()[1]]
            else:
                break

    def rowCount(self, parent=None):
        ncell = self.inmem.get_w_id('WAlarmTable').ncell
        occur_alarm_num = self.inmem.shmem.get_occur_alarm_nub()
        self.inmem.get_w_id('WAlarmTable').scrollToBottom()
        return ncell if ncell >= occur_alarm_num else occur_alarm_num

    def columnCount(self, parent=None, *args, **kwargs):
        return len(self.column_label)

    def db_is_not_empty(self, index):
        return len(self.dis_data) > (self.rowCount() - index.row() - 1)

    def get_row_values(self, index):
        return self.dis_data[self.rowCount() - index.row() - 1][index.column()]

    def get_row_alarm_name(self, index):
        return self.dis_data[self.rowCount() - index.row() - 1][-1] if self.db_is_not_empty(index) else ''

    def get_row_text(self, index):
        return self.get_row_values(index) if self.db_is_not_empty(index) else ''

    def get_row_paint_freeze(self, index):
        return self.get_row_alarm_name(index) in self.find_mismatch_list()

    def get_row_paint(self, index):
        if self.db_is_not_empty(index):
            if self.blick or self.get_row_paint_freeze(index):
                return QBrush(QColor(255, 204, 0))
            else:
                return QBrush(QColor(231, 231, 234))
        else:
            return QBrush((QColor(231, 231, 234)))

    def get_row_font_paint(self, index):
        if self.db_is_not_empty(index):
            if self.blick or self.get_row_paint_freeze(index):
                return QBrush(QColor(128, 128, 128))
            else:
                return QBrush(QColor(0, 0, 0))
        else:
            return QBrush(QColor(255, 255, 255))

    def data(self, index: QModelIndex, role: int = ...):
        if role == Qt.ItemDataRole.BackgroundRole:
            return self.get_row_paint(index)
        if role == Qt.ItemDataRole.TextColorRole:
            return self.get_row_font_paint(index)

        return f'{self.get_row_text(index)}' if role == Qt.ItemDataRole.DisplayRole else None

    def headerData(self, section: int, orientation: Qt.Orientation, role: int = ...):
        """ 행과 열의 이름 부분 """
        if orientation == Qt.Orientation.Horizontal and role == Qt.ItemDataRole.DisplayRole:
            header = self.column_label[section]
            return header




























