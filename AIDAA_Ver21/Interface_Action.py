from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from AIDAA_Ver21.Mem_ShMem import ShMem, InterfaceMem
from AIDAA_Ver21.Interface_ABCWidget import *


class Action(ABCWidget):
    def __init__(self, parent):
        super(Action, self).__init__(parent)
        self.setStyleSheet('background-color: rgb(100, 185, 211);')
        lay = QHBoxLayout(self)
        llay = QVBoxLayout()
        llay.addWidget(Action_alarm_area(self))
        llay.addWidget(Action_suggestion_area(self))
        rlay = QVBoxLayout()
        rlay.addWidget(Action_system_mimic_area(self))
        lay.addLayout(llay)
        lay.addLayout(rlay)

class Action_alarm_area(ABCWidget):
    def __init__(self, parent):
        super(Action_alarm_area, self).__init__(parent)
        self.setStyleSheet('background-color: rgb(149, 185, 211);')

class Action_suggestion_area(ABCWidget):
    def __init__(self, parent):
        super(Action_suggestion_area, self).__init__(parent)
        self.setStyleSheet('background-color: rgb(149, 100, 211);')
        
class Action_system_mimic_area(ABCWidget):
    def __init__(self, parent):
        super(Action_system_mimic_area, self).__init__(parent)
        self.setStyleSheet('background-color: rgb(149, 100, 100);')