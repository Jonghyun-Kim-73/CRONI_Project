import os
import sys
from datetime import datetime

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

ROOT_PATH = os.path.dirname(os.path.abspath(__file__))


class MainSysArea(QWidget):
    """ 시스템 디스플레이 위젯 """
    def __init__(self, parent, h, w):
        super(MainSysArea, self).__init__(parent)
        self.setAttribute(Qt.WA_StyledBackground, True)  # 상위 스타일 상속
        self.setObjectName('MainSysArea')
        # --------------------------------------------------------------------------------------------------------------
        self.setFixedHeight(h)
        self.setFixedWidth(w)
