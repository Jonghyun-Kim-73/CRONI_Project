import os
import sys
import math
from datetime import datetime

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


ROOT_PATH = os.path.dirname(os.path.abspath(__file__))


class MainSysRightArea(QWidget):
    def __init__(self, parent, x, y, w, h):
        super(MainSysRightArea, self).__init__(parent)
        self.mem = parent.mem
        self.MainSysLeftArea = parent.MainSysLeftArea
        # --------------------------------------------------------------------------------------------------------------
        self.setAttribute(Qt.WA_StyledBackground, True)  # 상위 스타일 상속
        self.installEventFilter(self)
        self.setObjectName('MainSysRightArea')
        # Size ---------------------------------------------------------------------------------------------------------
        self.setGeometry(x, y, w, h)
        self.setFixedHeight(h)
        self.setFixedWidth(w)
        # 테이블 셋업 ---------------------------------------------------------------------------------------------------
        p1 = QPushButton('CVCS', self)
        p1.setGeometry(0, 0, 400, 100)
        p1.clicked.connect(lambda a: self._go_sys('CVCS'))
        p2 = QPushButton('RCS', self)
        p2.setGeometry(0, 200, 400, 100)
        p2.clicked.connect(lambda a: self._go_sys('RCS'))

    def _go_sys(self, target_sys):
        self.MainSysLeftArea.update_sys_mimic(target_sys)