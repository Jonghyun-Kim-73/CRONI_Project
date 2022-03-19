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
                border-radius: 6px;
            }
            QTableWidget {
                color : white;
                background: rgb(231, 231, 234);
                border: 1px solid rgb(128, 128, 128);
                border-radius: 6px;
            }
            QPushButton{
                background: White;
                color: Black;
                border-radius:6px;
            }
            QHeaderView::section {
                background: rgb(128, 128, 128);
                font-size:14pt;
                border:0px solid;
            }
            QHeaderView {
                border:1px solid rgb(128, 128, 128);
                border-top-left-radius :6px;
                border-top-right-radius : 6px;
                border-bottom-left-radius : 0px;
                border-bottom-right-radius : 0px;
            }
            QTableView::item {
                padding:50px;
                font-size:14pt;
            }
            QScrollBar:vertical {
                width:30px;
            }
        """

    def __init__(self, parent):
        super(WLMain, self).__init__(parent)
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setStyleSheet(self.qss)
        layout = WithNoMargin(QVBoxLayout(self))
        layout.addWidget(WAlarmTable(self, hcell=36, ncell=24))     # hcell 는 3의 배수
        layout.addWidget(SuppressBTN('Suppress button', self))


class SuppressBTN(ABCPushButton):
    def __init__(self, str, parent):
        super(SuppressBTN, self).__init__(parent, str)
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setFixedHeight(34)
        self.clicked.connect(self.call_Suppress)

    def call_Suppress(self):
        self.inmem.get_w_id('WAlarmTableModel').remove_mismatch_alarm()


class WAlarmTable(ABCTableView, QTableView):
    def __init__(self, parent, hcell, ncell):
        super(WAlarmTable, self).__init__(parent)
        self.hcell, self.ncell = hcell, ncell
        self.setAttribute(Qt.WA_StyledBackground, True)
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
        self.setFixedHeight(self.hcell * (self.ncell + 1))

    def paintEvent(self, e: QPaintEvent) -> None:
        super(WAlarmTable, self).paintEvent(e)
        qp = QPainter(self.viewport())
        qp.save()
        # 가로선
        for i in range(self.ncell):
            pen_size = 2 if i % 5 == 0 else 1
            qp.setPen(QPen(QColor(128, 128, 128), pen_size))
            qp.drawLine(0, i * self.hcell, self.width(), i * self.hcell)
        # 세로선
        draw_acc = 0
        for j in range(self.model().columnCount()):
            qp.setPen(QPen(QColor(128, 128, 128), 1))
            draw_acc += self.columnWidth(j)
            qp.drawLine(draw_acc, 0, draw_acc, self.height())
        qp.restore()

    def call_double_click(self, index):
        alarm_des = self.inmem.shmem.get_alarm_des(self.inmem.get_w_id('WAlarmTableModel').get_row_alarm_name(index))

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
        fun_updater(self, 500, [self.update_alarm])

    def update_alarm(self):
        # TEST 로직
        if self.num_alarm == 2:
            self.inmem.shmem.change_shmem_val('UCCWIN', 1)
            self.inmem.shmem.change_shmem_db(self.inmem.shmem.mem)
        if self.num_alarm == 5:
            self.inmem.shmem.change_shmem_val('UCCWIN', -1)
            self.inmem.shmem.change_shmem_db(self.inmem.shmem.mem)
        if self.num_alarm == 20:
            self.inmem.shmem.change_shmem_val('UCCWIN', 1)
            self.inmem.shmem.change_shmem_db(self.inmem.shmem.mem)
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
                return QBrush(QColor(231, 230, 230))
        else:
            return QBrush(QColor(0, 0, 0))

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




























