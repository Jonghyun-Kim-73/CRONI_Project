from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from AIDAA_Ver21.Function_Mem_ShMem import ShMem, InterfaceMem
from AIDAA_Ver21.Interface_ABCWidget import *
from AIDAA_Ver21.Interface_Alarm import *
from AIDAA_Ver21.Interface_MainTabRight import *


class MainTabMain(ABCWidget, QWidget):
    def __init__(self, parent):
        super(MainTabMain, self).__init__(parent)
        self.setStyleSheet('background-color: rgb(188, 185, 211);')

        lay = QHBoxLayout(self)
        lay.addWidget(MainAlarm(self))
        lay.addWidget(MainTabRight(self))

