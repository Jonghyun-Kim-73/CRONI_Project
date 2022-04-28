from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from AIDAA_Ver21.Mem_ShMem import ShMem, InterfaceMem
from AIDAA_Ver21.Interface_ABCWidget import *


class MainTabSystem(ABCWidget, QWidget):
    def __init__(self, parent):
        super(MainTabSystem, self).__init__(parent)
        self.setStyleSheet('background-color: rgb(230, 184, 175);')
