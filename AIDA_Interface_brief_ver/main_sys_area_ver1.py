import os
import sys
import math
from datetime import datetime

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from AIDA_Interface_brief_ver.main_sys_area_r_ver1 import MainSysRightArea
from AIDA_Interface_brief_ver.main_sys_area_l_ver1 import MainSysLeftArea

ROOT_PATH = os.path.dirname(os.path.abspath(__file__))


class MainSysArea(QWidget):
    """ 시스템 디스플레이 위젯 """
    def __init__(self, parent, h, w):
        super(MainSysArea, self).__init__(parent)
        self.mem = parent.mem
        # --------------------------------------------------------------------------------------------------------------
        self.setAttribute(Qt.WA_StyledBackground, True)  # 상위 스타일 상속
        self.setObjectName('MainSysArea')
        # Size ---------------------------------------------------------------------------------------------------------
        self.setFixedHeight(h)
        self.setFixedWidth(w)
        # 테이블 셋업 ---------------------------------------------------------------------------------------------------
        self.MainSysRightArea = MainSysRightArea(self, 400, 0, w - 400, h)
        self.MainSysLeftArea = MainSysLeftArea(self, 0, 0, 400, h)

