from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from AIDAA_Ver21.Function_Mem_ShMem import ShMem, InterfaceMem
from AIDAA_Ver21.Interface_ABCWidget import *
from AIDAA_Ver21.Interface_Alarm import *
from AIDAA_Ver21.Interface_MainTabRight import *
import Interface_QSS as qss

class MainTabMain(ABCWidget):
    def __init__(self, parent):
        super(MainTabMain, self).__init__(parent)
        self.setStyleSheet(qss.Main_Tab)
        lay = QHBoxLayout(self)
        lay.setContentsMargins(10, 15, 10, 10)
        lay.addWidget(MainAlarm(self))
        lay.addWidget(MainTabRight(self))
        lay.setSpacing(10)

