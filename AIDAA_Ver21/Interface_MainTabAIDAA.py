from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from AIDAA_Ver21.Function_Mem_ShMem import ShMem, InterfaceMem
from AIDAA_Ver21.Interface_ABCWidget import *
from AIDAA_Ver21.Interface_Alarm import *
from AIDAA_Ver21.Interface_AIDAA_Diagnosis import *

class MainTabAIDAA(ABCWidget):
    def __init__(self, parent, widget_name=''):
        super().__init__(parent, widget_name)
        lay = QHBoxLayout(self)
        lay.setContentsMargins(10, 15, 10, 10)
        lay.addWidget(AIDAAAlarm(self))
        lay.addWidget(Diagnosis(self))
        lay.setSpacing(15)

