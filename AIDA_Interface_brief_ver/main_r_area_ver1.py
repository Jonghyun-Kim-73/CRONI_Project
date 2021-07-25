import os
import sys
from datetime import datetime

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

ROOT_PATH = os.path.dirname(os.path.abspath(__file__))


class MainRightArea(QWidget):
    """ 왼쪽 알람 디스플레이 위젯 """
    def __init__(self, parent, h, w, mem=None):
        super(MainRightArea, self).__init__(parent)
        self.mem = mem
        self.setAttribute(Qt.WA_StyledBackground, True)  # 상위 스타일 상속
        self.setObjectName('MainRightArea')
        # --------------------------------------------------------------------------------------------------------------
        self.setFixedHeight(h)
        self.setFixedWidth(w)