from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from AIDAA_Ver21.Function_Mem_ShMem import ShMem, InterfaceMem
from AIDAA_Ver21.Interface_ABCWidget import *
from AIDAA_Ver21.Interface_Alarm import *
from AIDAA_Ver21.Interface_AIDAA_Diagnosis import *

class MainTabAIDAA(ABCWidget):
    def __init__(self, parent):
        super(MainTabAIDAA, self).__init__(parent)
        lay = QHBoxLayout(self)
        lay.addWidget(AIDAAAlarm(self))
        lay.addWidget(Diagnosis(self))
        lay.setSpacing(5)

