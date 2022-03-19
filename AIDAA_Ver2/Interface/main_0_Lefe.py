import os
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import socket

from AIDAA_Ver2.TOOL.TOOL_Shmem import SHMem
from AIDAA_Ver2.TOOL.TOOL_Widget import *


class WLMain(ABCWidget):
    qss = """
            QWidget {
                background: rgb(231, 231, 234);
                border: 0px solid rgb(0, 0, 0); 
                font-size: 14pt;
                border-radius: 6px;
            }
            QPushButton{
                background: White;
                color: Black;
                border-radius:6px;
            }
            QScrollBar:vertical {
                width:30px;
            }
        """
    def __init__(self, parent):
        super(WLMain, self).__init__(parent)
        self.setStyleSheet(self.qss)
        layout = WithNoMargin(QVBoxLayout(self))
        # layout.addWidget(WAlarmTable(self, hcell=36, ncell=25))     # hcell 는 3의 배수
        layout.addWidget(WAlarmTable(self, hcell=36, ncell=9))     # hcell 는 3의 배수
        layout.addWidget(SuppressBTN('Suppress button', self))


class SuppressBTN(ABCPushButton):
    def __init__(self, str, parent):
        super(SuppressBTN, self).__init__(parent, str)
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setFixedHeight(34)
        self.clicked.connect(self.call_Suppress)

    def call_Suppress(self):
        print('Click SBTN')


class WAlarmTable(ABCTableView, QTableView):
    qss = """
        QTableView {
            color : white;
            background: rgb(231, 231, 234);
            border: none;
        }
        QHeaderView {
            border:1px solid rgb(128, 128, 128);
            border-top-left-radius :6px;
            border-top-right-radius : 6px;
            border-bottom-left-radius : 0px;
            border-bottom-right-radius : 0px;
        }
        QHeaderView::section {
            border: none;
            font-size:14pt;
            background: rgb(128, 128, 128);
        }
        
    """
    def __init__(self, parent, hcell, ncell):
        super(WAlarmTable, self).__init__(parent)
        self.hcell, self.ncell = hcell, ncell
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setStyleSheet(self.qss)
        self.setModel(WAlarmTableModel(self))
        self.set_Body()
        self.set_Horizontal()
        self.set_Vertical()

    def set_Horizontal(self):
        self.horizontalHeader().setDefaultAlignment(Qt.AlignmentFlag.AlignCenter)
        self.horizontalHeader().setFixedHeight(self.hcell)
        self.horizontalHeader().setDefaultSectionSize(self.hcell)
        self.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        [self.setColumnWidth(i+1, s) for i, s in enumerate([160, 160, 100, 100])]
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

    def set_Vertical(self):
        self.verticalHeader().hide()
        self.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Fixed)
        self.verticalHeader().setDefaultSectionSize(self.hcell)
        self.setVerticalScrollMode(QAbstractItemView.ScrollMode.ScrollPerPixel)
        self.verticalScrollBar().setSingleStep(self.hcell/3)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)

    def set_Body(self):
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


class WAlarmTableModel(ABCAbstractTableModel, QAbstractTableModel):
    column_label = ['DESCRIPTION', 'VALUE', 'SETPOINT', 'UNIT', 'DATE', 'TIME']
    num_alarm = 0

    def __init__(self, parent):
        super(WAlarmTableModel, self).__init__(parent)
        fun_updater(self, 1000, [self.update_alarm])

    def update_alarm(self):
        # TEST 로직
        if self.num_alarm == 4:
            self.inmem.shmem.change_shmem_val('UCCWIN', 1)
            self.inmem.shmem.change_shmem_db(self.inmem.shmem.mem)
        if self.num_alarm == 8:
            self.inmem.shmem.change_shmem_val('UCCWIN', -1)
            self.inmem.shmem.change_shmem_db(self.inmem.shmem.mem)
        self.num_alarm += 1
        # -----------------------------------------------------------
        self.alarm_cnt = self.inmem.shmem.get_occur_alarm_info()


        # layout 업데이트
        self.layoutAboutToBeChanged.emit()
        self.layoutChanged.emit()

    def rowCount(self, parent=None):
        ncell = self.inmem.get_w_id('WAlarmTable').ncell
        occur_alarm_num = self.inmem.shmem.get_occur_alarm_nub()
        return ncell if ncell >= occur_alarm_num else occur_alarm_num

    def columnCount(self, parent=None, *args, **kwargs):
        return len(self.column_label)

    def headerData(self, section: int, orientation: Qt.Orientation, role: int = ...):
        """ 행과 열의 이름 부분 """
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            header = self.column_label[section]
            return header
        # if orientation == Qt.Vertical and role == Qt.DisplayRole:
        #     return str(section + 1)
        return None


































