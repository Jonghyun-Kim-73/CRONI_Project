import os
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from AIDA_Interface_brief_ver.Thmem_qss_ver1 import qss
from AIDA_Interface_brief_ver.TOOL.TOOL_etc import p_

class Mainwindow(QWidget):
    """메인 윈도우"""
    def __init__(self, parent, mem=None):
        super(Mainwindow, self).__init__()
        self.mem = mem
        self.up_widget = parent
        # --------------------------------------------------------------------------------------------------------------
        self.setGeometry(300, 50, 1000, 800)
        self.setStyleSheet(qss)
        self.setObjectName('Mainwindow')

        self.set_main_frame()

    def set_main_frame(self):
        path = QPainterPath()
        path.addRoundedRect(QRect)

    def closeEvent(self, QCloseEvent):
        p_(__file__, 'Close')
        self.up_widget.closeEvent(QCloseEvent)