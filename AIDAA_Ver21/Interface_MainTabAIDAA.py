from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from AIDAA_Ver21.Interface_Diagnosis import Diagnosis
from AIDAA_Ver21.Mem_ShMem import ShMem, InterfaceMem
from AIDAA_Ver21.Interface_ABCWidget import *
from AIDAA_Ver21.Interface_Alarm import *
from AIDAA_Ver21.Interface_Diagnosis import *
import Interface_QSS as qss

class MainTabAIDAA(ABCWidget):
    def __init__(self, parent):
        super(MainTabAIDAA, self).__init__(parent)
        self.setStyleSheet(qss.AIDAA)
        self.setObjectName("BG")

        lay = QHBoxLayout(self)
        lay.setContentsMargins(5, 5, 5, 5)
        lay.addWidget(Alarm(self))
        lay.addWidget(Diagnosis(self))
        lay.setSpacing(5)

