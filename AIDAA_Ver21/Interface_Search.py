from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from AIDAA_Ver21.Mem_ShMem import ShMem, InterfaceMem
from AIDAA_Ver21.Interface_ABCWidget import *
from AIDAA_Ver21.Simulator_CNS import *

# ----------------------------------------------------------------------------------------------------------------------

class ProcedureSearch(ABCWidget, QWidget):
    def __init__(self, parent):
        super(ProcedureSearch, self).__init__(parent)
        self.setStyleSheet('background-color: rgb(212, 245, 211);')
        self.setGeometry(200, 200, 390, 300)
        lay = QVBoxLayout(self)
        lay.addWidget(ProcedureSearchWindow(self))

class ProcedureSearchWindow(ABCWidget, QWidget):
    def __init__(self, parent):
        super(ProcedureSearchWindow, self).__init__(parent)
        lay = QVBoxLayout(self)
        lay.addWidget(ProcedureSearchKeyword(self))
        lay.addWidget(ProcedureSearchNumber(self))

class ProcedureSearchKeyword(ABCLabel, QLabel):
    def __init__(self, parent):
        super(ProcedureSearchKeyword, self).__init__(parent)
        self.setText('키워드')

class ProcedureSearchNumber(ABCLabel, QLabel):
    def __init__(self, parent):
        super(ProcedureSearchNumber, self).__init__(parent)
        self.setText('절차서 번호')

# ----------------------------------------------------------------------------------------------------------------------

class SystemSearch(ABCWidget, QWidget):
    def __init__(self, parent):
        super(SystemSearch, self).__init__(parent)
        self.setStyleSheet('background-color: rgb(212, 245, 211);')
        self.setGeometry(200, 200, 390, 300)
        lay = QVBoxLayout(self)
        lay.addWidget(SystemSearchWindow(self))

class SystemSearchWindow(ABCWidget, QWidget):
    def __init__(self, parent):
        super(SystemSearchWindow, self).__init__(parent)
        lay = QVBoxLayout(self)
        lay.addWidget(SystemSearchName(self))

class SystemSearchName(ABCLabel, QLabel):
    def __init__(self, parent):
        super(SystemSearchName, self).__init__(parent)
        self.setText('시스템')

class XAISearch(ABCWidget, QWidget):
    def __init__(self, parent):
        super(XAISearch, self).__init__(parent)
        self.setStyleSheet('background-color: rgb(212, 245, 211);')
        self.setGeometry(200, 200, 390, 300)
        lay = QVBoxLayout(self)
        lay.addWidget(XAISearchWindow(self))

class XAISearchWindow(ABCWidget, QWidget):
    def __init__(self, parent):
        super(XAISearchWindow, self).__init__(parent)
        lay = QVBoxLayout(self)
        lay.addWidget(XAISearchName(self))

class XAISearchName(ABCLabel, QLabel):
    def __init__(self, parent):
        super(XAISearchName, self).__init__(parent)
        self.setText('XAI')