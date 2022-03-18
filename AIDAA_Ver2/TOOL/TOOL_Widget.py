from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from AIDAA_Ver2.TOOL.TOOL_Shmem import SHMem, make_shmem


def WithNoMargin(layout, c_m=0, s_m=0):
    layout.setContentsMargins(c_m, c_m, c_m, c_m)
    layout.setSpacing(s_m)
    return layout


class ABCWidget(QWidget):
    def __init__(self, parent):
        super(ABCWidget, self).__init__()
        self.shmem = make_shmem(parent, self)


class ABCPushButton(QPushButton):
    def __init__(self, parent, str):
        super(ABCPushButton, self).__init__(str)
        self.shmem = make_shmem(parent, self)