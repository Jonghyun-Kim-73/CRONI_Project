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
                padding:1px;
                padding-left:15px;
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
        self.setStyleSheet(self.qss)

        layout = WithNoMargin(QVBoxLayout(self))

        alarm_table = WAlarmTable(self)
        btn = SuppressBTN('Suppress button', self)

        layout.addWidget(alarm_table)
        layout.addWidget(btn)


class SuppressBTN(ABCPushButton):
    def __init__(self, str, parent):
        super(SuppressBTN, self).__init__(parent, str)
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setFixedHeight(34)
        self.clicked.connect(self.call_Suppress)

    def call_Suppress(self):
        print('Click SBTN')
        self.inmem.shmem.call_subpression()


class WAlarmTable(ABCTableView, QTableView):
    def __init__(self, parent):
        super(WAlarmTable, self).__init__(parent)
        self.setAttribute(Qt.WA_StyledBackground, True)

        # set the table model
        tm = WAlarmTableModel(self)
        self.setModel(tm)


class WAlarmTableModel(ABCAbstractTableModel, QAbstractTableModel):
    column_label = ['DESCRIPTION', 'VALUE', 'SETPOINT', 'UNIT', 'DATE', 'TIME']
    num_alarm = 0

    def __init__(self, parent):
        super(WAlarmTableModel, self).__init__(parent)
        #
        timer1 = QTimer(self)
        timer1.setInterval(1000)
        timer1.timeout.connect(self.update_alarm)
        timer1.start()

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


        # TODO 알람 리스트 업데이트 부분 만들기 ...



        # layout 업데이트
        self.layoutAboutToBeChanged.emit()
        self.layoutChanged.emit()

    def rowCount(self, parent=None):
        return self.inmem.shmem.get_occur_alarm_nub()

    def columnCount(self, parent=None, *args, **kwargs):
        return len(self.column_label)






































