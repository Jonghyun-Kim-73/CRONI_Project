from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from AIDAA_Ver21.Function_Mem_ShMem import ShMem, InterfaceMem
from AIDAA_Ver21.Interface_ABCWidget import *


class PreTrip(ABCWidget, QWidget):
    def __init__(self, parent):
        super(PreTrip, self).__init__(parent)
        self.setStyleSheet('background-color: rgb(212, 245, 211);')