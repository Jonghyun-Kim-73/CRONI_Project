import os
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import socket

from AIDAA_Ver2.TOOL.TOOL_Shmem import SHMem, make_shmem
from AIDAA_Ver2.TOOL.TOOL_Widget import ABCWidget, ABCPushButton, WithNoMargin


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
        self.clicked.connect(self.c)

    def c(self):

        print(self.shmem.show_w())


class WAlarmTable(ABCWidget):
    def __init__(self, parent):
        super(WAlarmTable, self).__init__(parent)
        self.setAttribute(Qt.WA_StyledBackground, True)