from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from AIDAA_Ver21.Mem_ShMem import ShMem, InterfaceMem
from AIDAA_Ver21.Interface_ABCWidget import *
from AIDAA_Ver21.Interface_Alarm import *
from AIDAA_Ver21.Interface_Diagnosis import *


class MainTabAIDAA(ABCWidget, QWidget):
    def __init__(self, parent):
        super(MainTabAIDAA, self).__init__(parent)
        self.setStyleSheet('background-color: rgb(213, 185, 211);')

        lay = QHBoxLayout(self)
        lay.addWidget(Alarm(self))
        lay.addWidget(Diagnosis(self))

