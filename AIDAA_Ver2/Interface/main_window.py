import os
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from AIDAA_Ver2.TOOL.TOOL_etc import p_
from ..TOOL.TOOL_Shmem import SHMem

import time

class Mainwindow(QWidget):
    """메인 윈도우"""
    def __init__(self, parent):
        super(Mainwindow, self).__init__()
        self.shmem = parent.shmem   # <- myform.shmem
        self.W_myform = parent
        self.selected_procedure: str = ''
        # --------------------------------------------------------------------------------------------------------------
        self.setGeometry(300, 50, 200, 200)
        # --------------------------------------------------------------------------------------------------------------
        # 프레임

    def set_frame(self):
        """ 메인프레임의 세팅 """
        pass

    def closeEvent(self, QCloseEvent):
        p_(__file__, 'Close')
        self.W_myform.closeEvent(QCloseEvent)